import chainlit as cl
import google.generativeai as genai
import os
from dotenv import load_dotenv
import mimetypes
import pdfplumber
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from docx import Document

# Disable auto-opening browser for server deployment
os.environ["CHAINLIT_NO_AUTO_LAUNCH"] = "true"

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY 

if not GEMINI_API_KEY:
    raise ValueError("⚠️ GEMINI_API_KEY not found. Please set it in a .env file.")

genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini Model
model_name = "gemini-1.5-flash"
model = genai.GenerativeModel(model_name)

# Initialize text splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

@cl.on_chat_start
async def on_chat_start():
    """Welcome message when the chat starts."""
    await cl.Message(content="👋 Welcome! Please upload files (text or image) to begin!").send()

@cl.on_message
async def main(message: cl.Message):
    """Handles user messages, file uploads, and answers questions."""
    chain = cl.user_session.get("chain")
    docsearch = cl.user_session.get("docsearch")
    uploaded_image_data = cl.user_session.get("uploaded_image_data")

    try:
        cl.logger.info(f"📩 Received message: {message.content}")

        # Process uploaded files (Images + Text)
        if message.elements:
            files = message.elements  
            texts, metadatas = [], []

            for file in files:

                # 📌 Improved MIME Type Detection
                file_type = file.mime if file.mime and file.mime != "file" else mimetypes.guess_type(file.name)[0] or "unknown"

                cl.logger.info(f"📂 Processing file: {file.name} - MIME Type: {file_type}")

                text = ""  # Initialize text variable

                # 🖼️ Process Image Files
                if file_type.startswith("image"):
                    with open(file.path, "rb") as image_file:
                        image_bytes = image_file.read()

                    if not image_bytes:
                        await cl.Message(content="⚠️ The uploaded image is empty. Try again.").send()
                        return

                    # ✅ Store image in session
                    uploaded_image_data = {
                        "mime_type": "image/jpeg",
                        "data": image_bytes
                    }

                    # 🔹 Extract text from image using Gemini Vision API
                    response = model.generate_content(["Extract information from this image:", uploaded_image_data])
                    extracted_text = response.text if response and response.text else "No text extracted."

                    cl.logger.info(f"✅ Extracted text from image: {len(extracted_text)} characters")
                    text = extracted_text  # Store extracted text for further processing

                # 📄 Handle Text File Processing
                elif file_type == "text/plain":
                    with open(file.path, "r", encoding="utf-8", errors="ignore") as f:
                        text = f.read().strip()

                elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    doc = Document(file.path)
                    text = "\n".join([p.text for p in doc.paragraphs])

                elif file_type == "pdf":
                    with pdfplumber.open(file.path) as pdf:
                        for page in pdf.pages:
                            page_text = page.extract_text()
                            if page_text is not None:
                                text += page_text.strip() + "\n"



                # Store extracted data in retriever
                if text:
                    split_texts = text_splitter.split_text(text)
                    texts.extend(split_texts)
                    metadatas.extend([{"source": f"{file.name}-{i}"} for i in range(len(split_texts))])
                    cl.logger.info(f"✅ Extracted text from {file.name}: {len(text)} characters")

            # 🔹 Store all extracted data (Text + Image Text) in `docsearch`
            if texts:
                embeddings = GoogleGenerativeAIEmbeddings(
                    google_api_key=GEMINI_API_KEY,
                    model="models/text-embedding-004"
                )

                if docsearch:
                    docsearch.add_texts(texts, metadatas=metadatas)
                    cl.logger.info("📝 Added new documents to existing retriever.")
                else:
                    docsearch = Chroma.from_texts(texts, embeddings, metadatas=metadatas)
                    cl.user_session.set("docsearch", docsearch)
                    cl.logger.info("🆕 Created new document retriever.")

                if not chain:
                    memory = ConversationBufferMemory(memory_key="chat_history", output_key="answer", return_messages=True)

                    chain = ConversationalRetrievalChain.from_llm(
                        ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0),
                        retriever=docsearch.as_retriever(),
                        memory=memory,
                        return_source_documents=True,
                    )
                    cl.user_session.set("chain", chain)
                    cl.logger.info("🔗 Created new conversational chain.")
                else:
                    chain.retriever = docsearch.as_retriever()
                    cl.user_session.set("chain", chain)
                    cl.logger.info("🔗 Updated conversational chain retriever.")

            await cl.Message(content="✅ Files processed! You can now ask questions.").send()
            return

        # Handle user queries
        if message.content:
            prompt = message.content

            # 🎨 Image-based Query
            if uploaded_image_data:
                try:
                    response = model.generate_content([prompt, uploaded_image_data])
                    if response.text:
                        await cl.Message(content=response.text).send()
                    else:
                        await cl.Message(content="❌ No relevant response from the image.").send()
                except Exception as e:
                    cl.logger.error(f"❌ Gemini API Error: {str(e)}")
                    await cl.Message(content="⚠️ Error while processing the image with Gemini API.").send()
                return  # Exit after processing image query

            # 📜 Text-based Query
            if docsearch and chain:
                res = await chain.ainvoke({"question": prompt})
                await cl.Message(content=res["answer"] if res["answer"] else "❌ No relevant answer found in the uploaded documents.").send()
                return

        await cl.Message(content="⚠️ No active session! Upload a file first.").send()

    except Exception as e:
        cl.logger.error(f"❌ Error in processing: {str(e)}")
        await cl.Message(content="⚠️ An error occurred while processing your request.").send()

# Ensure the app runs on the correct host and port for Render
if __name__ == "__main__":
    cl.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

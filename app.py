import google.generativeai as genai
import chainlit as cl
import os
from dotenv import load_dotenv
from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils import extract_text_from_file, image2base64

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

# Initialize text splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

# Initialize ChainLit app
@cl.on_chat_start
async def on_chat_start():
    """Welcome message when the chat starts."""
    msg = cl.Message(content="👋 Welcome! Please upload files 📂 to begin!")
    await msg.send()

@cl.on_message
async def main(message: cl.Message):
    """Handles user messages, processes file uploads, and answers questions."""
    chain = cl.user_session.get("chain")
    docsearch = cl.user_session.get("docsearch")  # Unified retriever for both text & images

    # Process new files if uploaded
    if message.elements:
        files = message.elements  # Multiple files
        supported_text_types = {"pdf", "vnd.openxmlformats-officedocument.wordprocessingml.document", "plain"}
        supported_image_types = {"jpeg", "png"}

        texts, metadatas = [], []

        for file in files:
            file_type = file.mime.split("/")[-1]

            # Handle text files
            if file_type in supported_text_types:
                text = extract_text_from_file(file.path, file_type)
                if text:
                    split_texts = text_splitter.split_text(text)
                    texts.extend(split_texts)
                    metadatas.extend([{"source": f"{file.name}-{i}"} for i in range(len(split_texts))])

            # Handle image files (store descriptions in Chroma)
            elif file_type in supported_image_types:
                base64_image = image2base64(file.path)
                if base64_image:
                    formatted_input = [
                        {
                            "role": "user",
                            "parts": [
                                {"inline_data": {"mime_type": "image/png", "data": base64_image}}
                            ]
                        }
                    ]
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(formatted_input)

                    image_description = f"File: {file.name}\n{response.text}"
                    texts.append(image_description)
                    metadatas.append({"source": f"Image-{file.name}"})

        # If text or image data is available, update retriever
        if texts:
            embeddings = GoogleGenerativeAIEmbeddings(
                google_api_key=GEMINI_API_KEY,
                model="models/text-embedding-004"
            )

            if docsearch:  # Append new documents if retriever already exists
                docsearch.add_texts(texts, metadatas=metadatas)
            else:  # Create a new document retriever
                docsearch = Chroma.from_texts(texts, embeddings, metadatas=metadatas)
                cl.user_session.set("docsearch", docsearch)

            # Create chain only if it does not exist
            if not chain:
                memory = ConversationBufferMemory(
                    memory_key="chat_history",
                    output_key="answer",
                    return_messages=True
                )

                chain = ConversationalRetrievalChain.from_llm(
                    ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0),
                    retriever=docsearch.as_retriever(),
                    memory=memory,
                    return_source_documents=True,
                )

                cl.user_session.set("chain", chain)
            else:
                # 🔹 Ensure the retriever is updated in the existing chain
                chain.retriever = docsearch.as_retriever()
                cl.user_session.set("chain", chain)

        # Send confirmation message
        await cl.Message(content="✅ Files processed! You can now ask questions.").send()
        return

    # Handle user queries
    if message.content:
        # **🔹 Ensure retriever fetches text & image descriptions**
        if docsearch and chain:
            res = await chain.ainvoke({"question": message.content})
            if res["answer"]:
                await cl.Message(content=res["answer"]).send()
            else:
                await cl.Message(content="❌ Sorry, no relevant answer found in the uploaded documents.").send()
            return

    # No valid session
    await cl.Message(content="❌ No active session! Upload a file first.").send()

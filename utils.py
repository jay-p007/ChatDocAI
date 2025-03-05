import pdfplumber
import base64
from docx import Document

# Function to extract text from uploaded file
def extract_text_from_file(file_path, file_type):
    text = ""
    if file_type == "pdf":
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
                # Extract hyperlinks if available
                for annot in page.annots:
                    if annot.get("uri"):
                        text += f"Link: {annot.get('uri')}\n"
    elif file_type == "vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    elif file_type == "plain":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    return text

# Function to convert image to Base64
def image2base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        print("Error encoding image:", e)
        return None
# ChatDocAI

ChatDocAI is an AI-powered chatbot that enables users to chat with their uploaded documents (PDFs, Word, TXT, and IMG) using **Google Gemini AI**. This tool leverages **Chainlit** to provide an interactive and intuitive interface for document-based conversations.

---

## **📌 Features**
- 📄 Upload and interact with documents (PDF, Word, TXT, Images).
- 🤖 AI-driven responses using **Google Gemini AI**.
- 🔍 Extract and summarize information from documents.
- 🏆 Easy-to-use **Chainlit** UI.
- 🚀 Fast and efficient processing of queries.

---

## **🛠 Prerequisites**
Before running the chatbot, ensure you have the following installed:
- **Python 3.8+**
- **pip (Python package manager)**
- **Git** (optional, for cloning the repository)

---

## **🚀 Installation Steps**
Follow these steps to set up and run ChatDocAI:

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/jay-p007/ChatDocAI.git
cd ChatDocAI
```

### **2️⃣ Create and Activate a Virtual Environment**
```bash
# On Windows
type nul > .env  # (Create an empty .env file if needed)
python -m venv venv
venv\Scripts\activate

# On Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Set Up Environment Variables**
Edit the `.env` file and add your **Google Gemini AI API Key**:
```
GEMINI_API_KEY=your_api_key_here
```

### **5️⃣ Run the Application**
```bash
chainlit run app.py
```

The ChatDocAI chatbot should now be running locally on **http://localhost:8000**.

---

## **📂 Project Structure**
```
ChatDocAI/
│-- app.py               # Main application file
│-- utils.py             # Helper functions
│-- requirements.txt     # Required dependencies
│-- chainlit.md          # Chainlit configuration file
│-- README.md            # Documentation
│-- .env                 # Environment variables (not committed)
│-- chroma_db/           # Vector database storage
```

---

## **💡 Usage Instructions**
1. Upload your document via the Chainlit interface.
2. Ask questions based on the content of the uploaded document.
3. Get instant responses powered by **Google Gemini AI**.

---

## **📌 License**
This project is **open-source** and available under the **MIT License**.

---

## **👨‍💻 Contributing**
Contributions are welcome! Feel free to open an issue or submit a pull request.

---
Enjoy using **ChatDocAI**! 🚀🎉


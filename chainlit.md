 
# Welcome to ChatDocAI 🚀🤖
---

### **Guide for Running ChatDocAI**

#### **ChatDocAI - Running with Chainlit**

- ChatDocAI is an AI-powered chatbot that allows users to chat with their uploaded documents (**PDFs, Word, TXT and Images**) using **Gemini AI**.  

This guide explains how to install dependencies and run the chatbot using **Chainlit**.

---

## **📌 Prerequisites**
Before running the chatbot, ensure you have the following installed:
- **Python 3.8+**  
- **pip (Python package manager)**  

---

## **🚀 Installation Steps**
Follow these steps to set up and run ChatDocAI:


### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/ChatDocAI.git
cd ChatDocAI
```

### **2️⃣ Create a Virtual Environment (Optional but Recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate      # On Windows
```

### **3️⃣ Install Required Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Set Up Environment Variables**
Create a `.env` file in the project root and add your **Gemini API key**:
```
GEMINI_API_KEY=your_gemini_api_key
```
Alternatively, rename `.env.example` to `.env` and fill in your API key.

### **5️⃣ Run the Chatbot**
Start ChatDocAI using Chainlit:
```bash
chainlit run app.py
```

### **6️⃣ Access the Chatbot**
After running the command, open your browser and go to:  
👉 **http://localhost:8000**  

You can now upload documents and chat with them! 📂🤖  

---

## **📚 Features**
✅ **Chat with documents** – Supports PDF, Word, and TXT.  
✅ **Multimodal support** – Understands text & images.  
✅ **Memory-based conversations** – Remembers previous chats.  
✅ **Fast and efficient** – Uses Google Gemini and ChromaDB.  

---

## **💡 Troubleshooting**
### **Issue: Module Not Found**
If you see an error like `ModuleNotFoundError: No module named 'chainlit'`, install dependencies:
```bash
pip install -r requirements.txt
```

### **Issue: Chainlit Not Found**
If Chainlit isn’t recognized, install it manually:
```bash
pip install chainlit
```

### **Issue: API Key Not Found**
Make sure your `.env` file exists and is correctly set up with `GEMINI_API_KEY`.

---

## **👨‍💻 Contributing**
Want to improve ChatDocAI? Feel free to submit a pull request! 🚀  

---

## **📜 License**
This project is licensed under the **MIT License**.

---

Enjoy chatting with your documents! 🎉



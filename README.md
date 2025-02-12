# PDF-Chatbot
# 📚 PDF Chatbot - AI-powered Document Question Answering

## 🚀 Overview
This project is an **AI-powered chatbot** that allows users to upload **PDF documents** and ask questions about their contents. It utilizes:
- **FastAPI** as the backend
- **Streamlit** as the frontend
- **HuggingFace models** for NLP-based answers
- **FAISS vector storage** for efficient document retrieval

---

## 📌 Features
✅ Upload a PDF document  
✅ Extract and store the text as **vector embeddings**  
✅ Ask questions and receive **AI-generated answers**  
✅ Uses **LangChain** for intelligent document querying  
✅ Supports **TinyLlama-1.1B** and other **HuggingFace models**  

---


---

## 🛠️ Installation & Setup

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/pdf-chatbot.git
cd pdf-chatbot


### **2️⃣ Install Dependencies**


Make sure you have Python 3.7+ installed. Then run:
pip install -r requirements.txt


### **3️⃣ Run the FastAPI Backend**

uvicorn app:app --reload
✅ API running at: http://127.0.0.1:8000


### **4️⃣ Run the Streamlit Frontend**

streamlit run app_frontend.py
✅ Frontend running at: http://localhost:8501



🏃 Usage

    Upload a PDF in the Streamlit interface
    Ask a question related to the document
    The chatbot retrieves relevant text and provides an AI-generated response


🔧 Docker Deployment

1️⃣ Install Docker

Make sure you have Docker installed. You can check with:
docker --version

2️⃣ Create a Dockerfile

Inside your project directory, create a Dockerfile:

# Use official Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy all files to container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the FastAPI and Streamlit ports
EXPOSE 8000 8501

# Start the API and Streamlit UI together
CMD uvicorn app:app --host 0.0.0.0 --port 8000 & streamlit run app_frontend.py --server.port 8501 --server.address 0.0.0.0

3️⃣ Build & Run the Docker Container

Build the image

docker build -t pdf-chatbot .

Run the container

docker run -p 8000:8000 -p 8501:8501 pdf-chatbot

✅ Now, visit:

    API: http://localhost:8000
    Streamlit UI: http://localhost:8501

import os
import fitz
from fastapi import FastAPI, File, UploadFile, HTTPException
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEndpoint
from langchain.llms import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


app = FastAPI()

# -Storage for PDFs and text data
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

vectorstore = None  # -Global vector store
llm = None  


def extract_text_from_pdf(pdf_path):

    """ Extract text from a given PDF file. """

    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text() 
    return text



def create_vectorstore(text):
    
    """ Convert extracted text into vector embeddings. """

    global vectorstore
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts([text], embeddings)


@app.on_event("startup")
def load_model():

    """   Load the AI model once at startup to prevent reloading on every request.   """

    global llm
    model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", low_cpu_mem_usage=True)

    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_length=512)
    llm = HuggingFacePipeline(pipeline=pipe)



@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):

    """   Handle PDF uploads and process text.   """


    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = extract_text_from_pdf(file_path)
    create_vectorstore(text)

    return {"message": "File uploaded and processed successfully", "filename": file.filename}



@app.post("/chat/")
async def chat(query: str):


    """   Chatbot API to answer questions based on PDF content.   """


    global vectorstore, llm

    if not vectorstore:
        raise HTTPException(status_code=400, detail="No document uploaded yet!")
    if not llm:
        raise HTTPException(status_code=500, detail="AI model not loaded!")

    qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever())

    response = qa_chain.run(query)
    return {"response": response}

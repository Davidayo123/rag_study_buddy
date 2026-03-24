from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import shutil
from dotenv import load_dotenv
import chromadb

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Load the secret API key
load_dotenv()
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY is missing! Please add it to your .env file.")

app = FastAPI(title="Dynamic Study Buddy API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Waking up the AI Engine...")

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
chroma_client = chromadb.PersistentClient(path="./chroma_db")
vector_db = Chroma(client=chroma_client, embedding_function=embeddings)
retriever = vector_db.as_retriever(search_kwargs={"k": 3})

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3, max_tokens=1024)

# Smarter prompt to handle missing information gracefully
system_prompt = """You are a helpful, expert tutor. 
You are given excerpts from uploaded documents to answer the student's question. 
WARNING: The text may contain random garbage characters or broken math from PDF extraction.
1. Ignore weird math symbols.
2. Read between the lines to find the actual concepts.
3. Write a fresh, simple, plain-English explanation.
4. DO NOT copy-paste garbled text. Write entirely in your own words.
5. If the answer is NOT in the provided context, DO NOT guess. Simply say: "I don't have information about that in the documents you've uploaded."

Context:
{context}"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{question}")
])

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print("AI Engine Online!")

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_tutor(request: QuestionRequest):
    try:
        answer = rag_chain.invoke(request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- THE NEW DYNAMIC UPLOAD PIPELINE ---
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    # 1. Save the uploaded file temporarily
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # 2. Read and slice the PDF
        loader = PyPDFLoader(temp_file_path)
        pages = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(pages)
        
        # 3. Translate to math and push to the database dynamically!
        vector_db.add_documents(chunks)
        
        # 4. Clean up the temporary file
        os.remove(temp_file_path)
        
        return {"message": f"Successfully processed '{file.filename}'! Added {len(chunks)} paragraphs to memory."}
        
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

# --- DIRECTORY MOUNT FOR FRONTEND ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")

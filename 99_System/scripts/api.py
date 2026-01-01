from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import uvicorn
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.embeddings import FakeEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# Load env
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configuration
LIFE_OS_PATH = os.getenv("LIFE_OS_PATH", os.path.expanduser("~/LifeOS"))
DB_DIR = os.path.join(LIFE_OS_PATH, "99_System", "vector_db")

security = HTTPBearer()
app = FastAPI(title="LifeOS API")

def get_vectordb():
    embeddings = FakeEmbeddings(size=1536)
    vectordb = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    return vectordb

def update_database():
    """
    Reads all Markdown files in LifeOS, splits them, 
    and updates the Vector Database.
    """
    print("🧠 Updating LifeOS Memory...")
    
    # 1. Load Markdown Files
    loader = DirectoryLoader(LIFE_OS_PATH, glob="**/*.md", loader_cls=TextLoader)
    documents = loader.load()
    
    if not documents:
        print("No documents found.")
        return

    # 2. Split Text (Chunks)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    # 3. Embed and Store
    vectordb = get_vectordb()
    # Clear existing documents that might have been loaded from files to ensure a clean re-index
    # Note: This is a simplistic approach. For more robust updates, consider tracking document versions/timestamps.
    existing_ids = vectordb.get(include=[])['ids']
    if existing_ids:
        vectordb.delete(ids=existing_ids)
    
    vectordb.add_documents(documents=texts)
    
    print(f"✅ Indexed {len(texts)} chunks of knowledge.")
    return vectordb

def verify_token(creds: HTTPAuthorizationCredentials = Depends(security)):
    if not API_TOKEN or creds.credentials != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    return True

class AddDocumentRequest(BaseModel):
    content: str
    metadata: dict = {}

class QueryDocumentsRequest(BaseModel):
    query_text: str
    k: int = 4

class UpdateDocumentRequest(BaseModel):
    content: str
    metadata: dict = {}

class Query(BaseModel):
    query: str

@app.post("/update")
def update_endpoint(_=Depends(verify_token)):
    try:
        vectordb = update_database()
        return {"status": "ok", "message": "Indexing completed."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/documents", status_code=201)
def add_document(request: AddDocumentRequest, _=Depends(verify_token)):
    try:
        vectordb = get_vectordb()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents([Document(page_content=request.content, metadata=request.metadata)])
        ids = vectordb.add_documents(documents=texts)
        return {"status": "ok", "message": "Document added.", "ids": ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/documents/search")
def search_documents(request: QueryDocumentsRequest, _=Depends(verify_token)):
    try:
        vectordb = get_vectordb()
        docs = vectordb.similarity_search(query=request.query_text, k=request.k)
        results = [{"id": doc.id, "content": doc.page_content, "metadata": doc.metadata} for doc in docs]
        return {"status": "ok", "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/documents/{doc_id}")
def update_document(doc_id: str, request: UpdateDocumentRequest, _=Depends(verify_token)):
    try:
        vectordb = get_vectordb()
        # Delete the old document
        vectordb.delete(ids=[doc_id])
        
        # Add the new document
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents([Document(page_content=request.content, metadata=request.metadata)])
        new_ids = vectordb.add_documents(documents=texts)
        
        return {"status": "ok", "message": "Document updated.", "old_id": doc_id, "new_ids": new_ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/documents/{doc_id}")
def delete_document(doc_id: str, _=Depends(verify_token)):
    try:
        vectordb = get_vectordb()
        vectordb.delete(ids=[doc_id])
        return {"status": "ok", "message": f"Document with ID {doc_id} deleted."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
def query_endpoint(body: Query, _=Depends(verify_token)):
    try:
        # from brain import ask_doppelganger
        # answer = ask_doppelganger(body.query)
        return {"status": "ok", "answer": "No answer available."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

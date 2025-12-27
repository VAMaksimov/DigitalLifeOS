import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configuration
# Allow overriding the LifeOS path from the environment for integration (n8n, agents)
LIFE_OS_PATH = os.getenv("LIFE_OS_PATH", os.path.expanduser("~/LifeOS"))
DB_DIR = os.path.join(LIFE_OS_PATH, "99_System", "vector_db")

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
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    # Create or update ChromaDB
    vectordb = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    print(f"✅ Indexed {len(texts)} chunks of knowledge.")
    return vectordb

def ask_doppelganger(query):
    """
    Queries the database using an LLM.
    """
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectordb = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, 
        chain_type="stuff", 
        retriever=retriever,
        return_source_documents=True
    )
    
    result = qa_chain.invoke({"query": query})
    return result['result']

if __name__ == "__main__":
    # Uncomment the next line to run a full re-index
    # update_database()
    
    # Test the brain
    while True:
        q = input("\n🗣️  Ask your Doppelganger: ")
        if q.lower() in ["exit", "quit"]: break
        answer = ask_doppelganger(q)
        print(f"🤖 Doppelganger: {answer}")
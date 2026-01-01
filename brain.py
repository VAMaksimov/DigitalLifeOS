import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configuration
# Allow overriding the LifeOS path from the environment for integration (n8n, agents)
LIFE_OS_PATH = os.getenv("LIFE_OS_PATH", os.path.expanduser("~/LifeOS"))
DB_DIR = os.path.join(LIFE_OS_PATH, "99_System", "vector_db")


def ask_doppelganger(query):
    # Placeholder function since the actual implementation is commented out
    return "This is a placeholder answer."

# def ask_doppelganger(query):
#     """
#     Queries the database using an LLM.
#     """
#     embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
#     vectordb = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    
#     llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    
#     retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    
#     qa_chain = RetrievalQA.from_chain_type(
#         llm=llm, 
#         chain_type="stuff", 
#         retriever=retriever,
#         return_source_documents=True
#     )
    
#     result = qa_chain.invoke({"query": query})
#     return result['result']

if __name__ == "__main__":
    # Test the brain
    while True:
        q = input("\n🗣️  Ask your Doppelganger: ")
        if q.lower() in ["exit", "quit"]: break
        answer = ask_doppelganger(q)
        print(f"🤖 Doppelganger: {answer}")
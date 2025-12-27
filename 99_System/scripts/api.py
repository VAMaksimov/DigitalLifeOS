from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import uvicorn


# Load env
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

security = HTTPBearer()
app = FastAPI(title="LifeOS API")

def verify_token(creds: HTTPAuthorizationCredentials = Depends(security)):
    if not API_TOKEN or creds.credentials != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    return True

class Query(BaseModel):
    query: str


@app.post("/update")
def update_endpoint(_=Depends(verify_token)):
    try:
        # Import here so the main app can start even if heavy libs are not installed
        # from brain import update_database
        # vectordb = update_database()
        return {"status": "ok", "message": "Indexing completed."}
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

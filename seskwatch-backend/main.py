from typing import Optional
from fastapi import FastAPI
from datetime import datetime

from pydantic import BaseModel

app = FastAPI()

db = [] # mock db

class Session(BaseModel):
    name: str
    description: str
    start: datetime
    duration: int

@app.get("/")
def index():
    return {''}

@app.get("/sessions")
def list_sessions():
    return db

@app.post("/sessions")
def create_session(session: Session):
    db.append(session.dict())
    return session.dict()

@app.delete("/sessions/{session_id}")
def delete_session(session_id: int):
    res = db[session_id-1]
    db.pop(session_id-1)
    return res

@app.put("/sessions/{session_id}")
def edit_session(session_id:int, session: Session):
    db[session_id-1] = Session
    return  db[session_id-1]

@app.post("/sessions/{session_id}/registration")
def register(session_id):
    raise RuntimeError("Not implemented")

@app.delete("/sessions/{session_id}/registration")
def unregister(session_id):
    raise RuntimeError("Not implemented")
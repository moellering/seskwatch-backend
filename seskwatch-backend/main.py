from typing import Optional
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return {''}


@app.get("/sessions")
def list_sessions():
    return [{"id": '1', "name": "testsession"}]


@app.post("/sessions")
def create_session():
    return [{"id": '1', "name": "testsession"}]

@app.put("/sessions/{session_id}")
def edit_session():
    return [{"id": '1', "name": "testsession"}]

@app.post("/sessions/{session_id}/registration")
def register(session_id):
    return {}

@app.delete("/sessions/{session_id}/registration")
def unregister(session_id):
    return {}
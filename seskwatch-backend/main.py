from typing import Optional
from fastapi import FastAPI
from datetime import datetime

from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator


app = FastAPI()

db = [] # mock db

class Session(Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(50)
    description = fields.CharField(50)
    start = fields.DatetimeField()
    duration = fields.IntField(constraints={"minimum": 0})

Session_Pydantic = pydantic_model_creator(Session, name='Session')
SessionIn_Pydantic = pydantic_model_creator(Session, name='SessionIn', exclude_readonly=True)


@app.get("/")
def index():
    return {''}

@app.get("/sessions")
async def list_sessions():
    return await Session_Pydantic.from_queryset(Session.all())

@app.post("/sessions")
async def create_session(session: SessionIn_Pydantic):
    session_obj = await Session.create(**session.dict()) #exclude_unset=True if optional nullable fields are present
    return await Session_Pydantic.from_tortoise_orm(session_obj)

@app.delete("/sessions/{session_id}")
def delete_session(session_id: int):
    res = db[session_id]
    db.pop(session_id)
    return res

@app.put("/sessions/{session_id}")
def edit_session(session_id:int, session: SessionIn_Pydantic):
    db[session_id] = session
    return  db[session_id].dict()

@app.post("/sessions/{session_id}/registration")
def register(session_id):
    raise RuntimeError("Not implemented")

@app.delete("/sessions/{session_id}/registration")
def unregister(session_id):
    raise RuntimeError("Not implemented")


register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['main']},
    generate_schemas=True,
    add_exception_handlers=True
)
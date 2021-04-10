from typing import Optional
from fastapi import FastAPI
from datetime import datetime

from uuid import UUID

from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise import Tortoise


app = FastAPI()

class SessionType(Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(50)
    icon = fields.CharField(20)



class Flag(Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(100)


class Session(Model):
    id = fields.UUIDField(pk=True)
    title = fields.CharField(100)
    description = fields.CharField(500)
    start = fields.DatetimeField()
    duration_minutes = fields.IntField(constraints={"minimum": 0})
    person_name = fields.CharField(100)
    status = fields.CharField(10)
    max_ppl = fields.IntField(constraints={"minimum": 0})
    video_url = fields.CharField(200)

    type = fields.ForeignKeyField('models.SessionType')
    flags = fields.ManyToManyField('models.Flag', related_name='sessions')

    def registered_people(self) -> int:
        return 1 # todo -> 1 is dummy value

    class PydanticMeta:
        computed = ('registered_people', )
    




Tortoise.init_models(["main"], "models")

Session_Pydantic = pydantic_model_creator(Session, name='Session')
SessionIn_Pydantic = pydantic_model_creator(Session, name='SessionIn', exclude_readonly=True)

from pprint import pprint
pprint(Session_Pydantic.schema())
pprint(SessionIn_Pydantic.schema())

SessionType_Pydantic = pydantic_model_creator(SessionType, name='SessionType')
SessionTypeIn_Pydantic = pydantic_model_creator(SessionType, name='SessionTypeIn', exclude_readonly=True)

Flag_Pydantic = pydantic_model_creator(Flag, name='Flag')
FlagIn_Pydantic = pydantic_model_creator(Flag, name='FlagIn', exclude_readonly=True)


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
async def delete_session(session_id: UUID):
    await Session.filter(id=session_id).delete()
    return {}

@app.put("/sessions/{session_id}")
async def edit_session(session_id: UUID, session: SessionIn_Pydantic):
    session_obj = await Session.filter(id=session_id).first()
    session_obj.update_from_dict(session.dict())
    await session_obj.save()
    return await Session_Pydantic.from_tortoise_orm(session_obj)

@app.post("/sessions/{session_id}/registration")
def register(session_id: UUID):
    raise RuntimeError("Not implemented")

@app.delete("/sessions/{session_id}/registration")
def unregister(session_id: UUID):
    raise RuntimeError("Not implemented")





@app.get("/flags")
async def list_flags():
    return await Flag_Pydantic.from_queryset(Flag.all())

@app.post("/flags")
async def create_flag(flag: FlagIn_Pydantic):
    flag_obj = await Flag.create(**flag.dict()) #exclude_unset=True if optional nullable fields are present
    return await Flag_Pydantic.from_tortoise_orm(flag_obj)



@app.get("/types")
async def list_session_types():
    return await SessionType_Pydantic.from_queryset(SessionType.all())

@app.post("/types")
async def create_session_type(session_type: SessionTypeIn_Pydantic):
    session_type_obj = await SessionType.create(**session_type.dict()) #exclude_unset=True if optional nullable fields are present
    return await SessionType_Pydantic.from_tortoise_orm(session_type_obj)




register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['main']},
    generate_schemas=True,
    add_exception_handlers=True
)
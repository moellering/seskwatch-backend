from typing import Optional
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/sessions/")
def read_item():
    return [{"id": '1', "name": "testsession"}]
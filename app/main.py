from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
import requests


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


class Item(BaseModel):
    q: Optional[str] = None


@app.post("/items/{item_id}")
def request_items(item_id: int, item: Item):
    host = '127.0.0.1'
    r = requests.get(f'http://{host}/items/{item_id}', params={'q': item.q})
    return r.json()

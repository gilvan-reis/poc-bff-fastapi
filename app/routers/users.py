from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel
import requests

router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}


class User(BaseModel):
    q: Optional[str] = None


@router.post("/users/{username}", tags=["users"])
async def request_items(username: str, token: str, user: User):
    host = '127.0.0.1'
    r = requests.get(f'http://{host}/users/{username}?token={token}')
    return r.json()

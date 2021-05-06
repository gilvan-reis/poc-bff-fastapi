from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
import requests

from app.modules.users.dependencies import get_current_active_user
from app.modules.users.schemas import User


users_router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@users_router.get('/')
@cache(namespace='read_users', expire=60)
async def read_users():
    print('users requested')
    return [{'username': 'Rick'}, {'username': 'Morty'}]


@users_router.get('/{username}')
async def read_user(username: str):
    return {'username': username}


@users_router.post('/{username}')
async def request_user(username: str, token: str):
    host = '127.0.0.1'
    r = requests.get(f'http://{host}/users/{username}?token={token}')
    return r.json()


@users_router.get('/me/', response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@users_router.get('/me/items/')
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{'item_id': 'Foo', 'owner': current_user.username}]

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
    return [{'username': 'johndoe'}, {'username': 'alice'}]


@users_router.get('/{username}')
async def read_user(username: str):
    if username == 'alice':
        return {
            'username': 'alice',
            'email': 'alice@example.com',
            'hashed_password': 'XXX',
        }

    return {'username': username}


@users_router.get('/item')
async def read_last_user_item():
    host = '127.0.0.1:3021'

    response = requests.get(f'http://{host}/users/', timeout=4)
    users = response.json()

    username = users[-1]['username']
    response = requests.get(f'http://{host}/users/{username}', timeout=4)
    result = response.json()
    del result['hashed_password']

    item_id = 'gun'
    token = 'jessica'
    headers = {'X-Token': 'secret-token'}
    response = requests.get(
        f'http://{host}/items/{item_id}?token={token}', headers=headers, timeout=4)
    item = response.json()
    result['item_name'] = item['name']

    return result


@users_router.get('/me/', response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@users_router.get('/me/items/')
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{'item_id': 'Foo', 'owner': current_user.username}]

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache
from jose import JWTError
from pydantic import BaseModel
import requests

from app.dependencies import decode_jwt_payload, oauth2_scheme, verify_password


fake_users_db = {
    'johndoe': {
        'username': 'johndoe',
        'full_name': 'John Doe',
        'email': 'johndoe@example.com',
        'hashed_password': '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',  # secret
        'disabled': False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": True,
    },
}


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False

    if not verify_password(password, user.hashed_password):
        return False

    return user


def authenticate_user_in_fake_db(username: str, password: str):
    return authenticate_user(fake_users_db, username, password)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode_jwt_payload(token)
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = get_user(fake_users_db, username=username)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail='Inactive user')

    return current_user


router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.get('/')
@cache(namespace='users', expire=60)
async def read_users():
    print('users requested')
    return [{'username': 'Rick'}, {'username': 'Morty'}]


@router.get('/{username}')
async def read_user(username: str):
    return {'username': username}


@router.post('/{username}')
async def request_items(username: str, token: str):
    host = '127.0.0.1'
    r = requests.get(f'http://{host}/users/{username}?token={token}')
    return r.json()


@router.get('/me/', response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get('/me/items/')
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{'item_id': 'Foo', 'owner': current_user.username}]

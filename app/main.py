from fastapi import Depends, FastAPI, HTTPException, status
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.dependencies import create_access_token, get_token_header
from app.internal import admin
from app.routers import items, users

app = FastAPI()


@app.on_event('startup')
async def startup():
    FastAPICache.init(InMemoryBackend(), prefix='fastapi-cache')


app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix='/admin',
    tags=['admin'],
    dependencies=[Depends(get_token_header)],
    responses={418: {'description': "I'm a teapot"}},
)


@app.get('/')
async def root():
    return {'message': 'Hello Bigger Applications!'}


class ClearCacheParams(BaseModel):
    namespace: str


@app.post('/clear')
async def clear_cache(params: ClearCacheParams):
    print(f'clearing namespace: {params.namespace}')
    return await FastAPICache.clear(namespace=params.namespace)


class Token(BaseModel):
    access_token: str
    token_type: str


@app.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users.authenticate_user_in_fake_db(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    access_token = create_access_token(data={'sub': user.username})
    return {'access_token': access_token, 'token_type': 'bearer'}

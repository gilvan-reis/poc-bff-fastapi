from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_cache import FastAPICache

from app.modules.dependencies import create_access_token
from app.modules.schemas import ClearCacheParams, Token
from app.modules.users.dependencies import authenticate_user_in_fake_db


root_router = APIRouter()


@root_router.get('/')
async def root():
    return {'message': 'Hello Bigger Applications!'}


@root_router.post(
    '/clear',
    responses={
        200: {'description': 'Return the number of cleaned cache in the given namespace.'},
    },
)
async def clear_cache(params: ClearCacheParams):
    print(f'clearing namespace: {params.namespace}')
    return await FastAPICache.clear(namespace=params.namespace)


@root_router.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user_in_fake_db(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    access_token = create_access_token(data={'sub': user.username})
    return {'access_token': access_token, 'token_type': 'bearer'}

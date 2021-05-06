from fastapi import Depends, FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from app.modules.admin.router import admin_router
from app.modules.dependencies import get_token_header
from app.modules.items.router import items_router
from app.modules.router import root_router
from app.modules.users.router import users_router


app = FastAPI(
    title='POC BFF FastApi',
    description='This project test the utilization of FastApi as a BFF',
    version='1.0.0',
)


@app.on_event('startup')
async def startup():
    FastAPICache.init(InMemoryBackend(), prefix='fastapi-cache')


app.include_router(root_router)
app.include_router(users_router)
app.include_router(items_router)
app.include_router(
    admin_router,
    prefix='/admin',
    tags=['admin'],
    dependencies=[Depends(get_token_header)],
    responses={418: {'description': "I'm a teapot"}},
)

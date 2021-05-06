from fastapi import APIRouter


admin_router = APIRouter()


@admin_router.post('/')
async def update_admin():
    return {'message': 'Admin getting schwifty'}

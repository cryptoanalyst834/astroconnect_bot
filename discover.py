from fastapi import APIRouter
from database import get_all_users

router = APIRouter()

@router.get("/profiles")
async def profiles():
    users = await get_all_users()
    return users

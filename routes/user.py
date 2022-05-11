import imp
from fastapi import APIRouter

from models.user import User
from config.db import conn

user = APIRouter()


@user.get("/")
async def find_all_users():
    return conn.local.user.find()

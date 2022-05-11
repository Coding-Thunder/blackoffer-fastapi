from pydantic import BaseModel

from models.users.model import Users
from passlib.context import CryptContext
import json


class NewUser(BaseModel):
    username: str
    password: str


def crete_new_user(new_user):
    user = Users(username=new_user.username,
                 password=get_password_hash(new_user.password))
    user.save()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(name, password):
    user = json.loads(Users.objects.get(username=name).to_json())
    if user:
        password_check = pwd_context.verify(password, user["password"])
        return password_check
    else:
        return False

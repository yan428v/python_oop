import json
import os.path
import re

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, field_validator
from datetime import date

app = FastAPI()


class UserInfo(BaseModel):
    last_name: str
    first_name: str
    birth_date: date
    number: str
    mail: EmailStr

    @field_validator('last_name', 'first_name')
    @classmethod
    def name_validate(cls, value: str) -> str:

        if not value[0].isupper():
            raise ValueError("должно начинаться с заглавной буквы")


        if not re.match(r'^[А-ЯЁ][а-яё]+$', value):
            raise ValueError("только кириллица")

        return value

@app.post("/user")
def create_user(req: UserInfo):
    user = {
    "last_name": req.last_name,
    "first_name": req.first_name,
    "birth_date": str(req.birth_date),
    "number": req.number,
    "mail": req.mail
    }

    filename = "user.json"

    if os.path.exists(filename):
        with open(filename, 'r', encoding="utf-8") as f:
            users = json.load(f)
    else:
        users = []

    users.append(user)

    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


    return "данные успешно сохранены"

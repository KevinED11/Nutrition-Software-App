from fastapi import APIRouter, HTTPException
from models.database.Users import Users
from models.read.UserRead import UserRead
from config.db_connection import engine
from sqlmodel import Session, select
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from typing import Optional

filterUsers = APIRouter(tags=["Users"])

@filterUsers.get("/users/filter", response_model=list[UserRead], status_code=HTTP_200_OK)
async def filter_user(name: Optional[str] = None, age: Optional[int] = None):
    with Session(engine) as session:
        if name and age:
            #return users o user with age and name is not None
            users_filter: list[Users | None] = session.exec(select(Users).where( (Users.name == name) & (Users.age == age) )).all()
            if users_filter:
                return users_filter

            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

        elif name:
            users_filter: list[Users | None] = session.exec(select(Users).where( (Users.name == name) )).all()
            if users_filter:
                return users_filter
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

        elif age:
            users_filter: list[Users | None] = session.exec(select(Users).where( (Users.age == age) )).all()
            if users_filter:
                return users_filter
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")










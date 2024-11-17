import os
from typing import Literal

from pydantic import BaseModel

from app.settings import session, SERVICE_KEY


class UserSchema(BaseModel):
    id: int
    shkolo_username: str
    shkolo_name: str
    pupil_id: int
    coins: int
    bulbs: int
    type: int


class UserCreate(BaseModel):
    shkolo_username: str = None
    shkolo_name: str = None
    pupil_id: int
    coins: int = None
    bulbs: int = None


class UsersBridge:
    base_url = os.environ["USERS_MS_URL"]

    @classmethod
    async def create(cls, payload: UserCreate) -> UserSchema:
        async with session.post(cls.base_url + "/users/", json=payload.model_dump()) as resp:
            content = await resp.json()

            if resp.status == 422:
                raise ValueError(content)

            return content

    @staticmethod
    async def _fetch_user(url) -> UserSchema:
        async with session.get(url) as resp:
            data = await resp.json()

            return UserSchema(**data) if data else None

    @classmethod
    async def get_by_id(cls, id_: int) -> UserSchema:
        url = cls.base_url + f"/users/{id_}"

        return await cls._fetch_user(url)

    @classmethod
    async def get_by_username(cls, username: str) -> UserSchema:
        url = cls.base_url + f"/users/username/{username}"

        return await cls._fetch_user(url)

    @classmethod
    async def get_by_pupil_id(cls, id_: int) -> UserSchema:
        url = cls.base_url + f"/users/pupil_id/{id_}"

        return await cls._fetch_user(url)

    @classmethod
    async def inc_currency(cls, id_: int, currency: Literal["coins","bulbs"], value: int) -> int:
        url = cls.base_url + f"/users/{id_}/{currency}/add?value={value}"

        async with session.post(url, headers={"service-key": SERVICE_KEY}) as resp:
            resp.raise_for_status()

            return await resp.json()

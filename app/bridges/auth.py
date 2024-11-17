import os

from app.bridges.users import UserSchema
from app.settings import session


class AuthBridge:
    base_url = os.environ["AUTH_MS_URL"]

    @staticmethod
    async def _fetch_user(url, **kwargs) -> UserSchema:
        async with session.get(url, **kwargs) as resp:
            resp.raise_for_status()

            data = await resp.json()

            return UserSchema(**data) if data else None

    @classmethod
    async def get_current_user(cls, token: str) -> UserSchema:
        url = cls.base_url + f"/auth/get-current-user"

        return await cls._fetch_user(url, headers={"Authorization": "Bearer " + token})

    @classmethod
    async def get_current_admin(cls, token: str) -> UserSchema:
        url = cls.base_url + f"/auth/get-current-admin"

        return await cls._fetch_user(url, headers={"Authorization": "Bearer " + token})

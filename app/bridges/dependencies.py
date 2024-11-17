from typing import Annotated

import aiohttp.client_exceptions
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.bridges.auth import AuthBridge
from app.bridges.users import UserSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserSchema:
    return await AuthBridge.get_current_user(token)

async def get_current_admin(token: Annotated[str, Depends(oauth2_scheme)]) -> UserSchema:
    try:
        return await AuthBridge.get_current_admin(token)
    except aiohttp.client_exceptions.ClientResponseError as e:
        raise HTTPException(
            status_code=e.status,
            detail=e.message
        )

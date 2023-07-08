from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from auth.utils import decode_token

from app.schemas import Session


async def _check_token(
    token_type: str,
    credentials: HTTPAuthorizationCredentials,
) -> Session:
    token = credentials.credentials

    if not token:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials.',
        )

    claims = decode_token(token)

    if claims is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='Invalid token or expired token.')

    if claims.get('type') != token_type:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='Invalid token.')

    return Session(username=claims.get('sub'), profile=claims.get('profile'))


async def check_access_token(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> Session:
    return await _check_token(
        'a',
        credentials,
    )


async def check_refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> Session:
    return await _check_token(
        'r',
        credentials,
    )


async def is_admin_session(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> Session:
    session = await check_access_token(credentials)

    if not session.profile.is_admin:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail='Not authorized.')

    return session

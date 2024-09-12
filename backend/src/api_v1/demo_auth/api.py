import uuid
from time import time
from typing import Any, NoReturn

from fastapi import APIRouter, Depends, HTTPException, Header, Cookie
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette import status
from starlette.responses import Response

router = APIRouter(prefix="/demo_auth", tags=["demo_auth"])
security = HTTPBasic()

user_map = {
    "admin": "123",
    "john": "321",
}
static_token_map = {
    "b19f62bb798a3b20041feec98d6f4c": "admin",
    "feec98d6f4cb19f62bb798a3b20041": "john",
}


async def get_user_username(
    credentials: HTTPBasicCredentials = Depends(security),
):
    if found_password := user_map.get(credentials.username):
        if found_password == credentials.password:
            return credentials.username

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={"WWW-Authenticate": "Basic"},
    )


@router.get("/hello", response_model=dict)
async def home_page(username: str = Depends(get_user_username)):
    return {"message": f"Hello little {username}"}


async def get_username_by_token(
    static_token: str = Header(alias="x-auth-token"),
) -> str:
    if username := static_token_map.get(static_token):
        return username

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.get("/token")
async def token_auth(username: str = Depends(get_username_by_token)) -> dict:
    return {"username": username}


COOKIES_DICT: dict[str, dict[str, Any]] = {}  # DATABASE
COOKIE_SESSION_ID_KEY = "web-app-session_id"


def generate_session_id() -> str:
    return str(uuid.uuid4())


@router.post(
    "/login-cookie",
    response_model=dict,
    # Check that user is authenticated
)
async def login_cookie(
    response: Response,
    username: str = Depends(get_username_by_token),
):
    session_id = generate_session_id()

    # add session_id to database
    COOKIES_DICT[session_id] = {
        "username": username,
        "login_at": int(time()),
    }

    # add session to client
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)

    return {"result": "ok"}


async def get_authenticated_user_name(
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
) -> dict | NoReturn:
    if session := COOKIES_DICT.get(session_id):
        return session

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get(
    "/hello-world/",
    response_model=dict,
)
async def hello_world(session: dict = Depends(get_authenticated_user_name)):
    return {
        "message": f"Hello, {session['username']}",
        **session,
    }


@router.post(
    "/logout",
    response_model=dict,
)
async def logout(
    response: Response,
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
):
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    session = COOKIES_DICT.pop(session_id)
    return {
        "message": f"{session["username"]} logged out",
    }

import hashlib
import hmac
from os import getenv

from dotenv import load_dotenv
from fastapi import APIRouter, Response
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)

load_dotenv()
TOKEN = (getenv("BOT_TOKEN"))
SECRET = "SECRET_KEY_HERE"
BOT_TOKEN = TOKEN
router = APIRouter()
cookie_transport = CookieTransport(cookie_name="fastapiusersauth",
                                   cookie_max_age=3600)


async def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt-cookie",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)


async def add_cookie_user_login(user_id: int, response: Response):
    response.set_cookie(
        key="user_id",
        value=str(user_id),
        httponly=True,
        max_age=3600
    )
    return {"status": "ok", "message": "Logged in"}


async def verify_telegram_data(user_data: dict):
    received_hash = user_data.get('hash')

    if not received_hash:
        return False

    auth_data = []

    for key, value in sorted(user_data.items()):
        if key != 'hash':
            auth_data.append(f"{key}={value}")

    data_check_string = "\n".join(auth_data)

    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()

    expected_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected_hash, received_hash)

from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, Response

from utils.utils_servers_api import ResponseApiServers

router = APIRouter()


@router.get('/', response_class=HTMLResponse)
async def index(request: Request):
    response = ResponseApiServers()
    return await response.index(request=request)


@router.post('/login')
async def login(user: dict, response: Response):
    login_response = ResponseApiServers()
    return await login_response.login(user=user, response=response)


@router.get('/main_menu', response_class=HTMLResponse)
async def main_menu(request: Request):
    response = ResponseApiServers()
    return await response.main_menu(request=request)


@router.get('/servers', response_class=HTMLResponse)
async def servers(request: Request):
    try:
        user_id = int(request.cookies.get("user_id"))
        response = ResponseApiServers(user_id=user_id)
        return await response.servers(request=request)
    except Exception as e:
        return f"Error: {e}"


@router.get('/servers/add')
async def get_add_server(request: Request):
    response = ResponseApiServers()
    return await response.get_add_server(request=request)


@router.post('/servers/add')
async def post_add_server(
        request: Request,
        password: Annotated[str, Form()],
        ip: Annotated[str, Form()],
        response_class=HTMLResponse
    ):
    try:
        user_id = int(request.cookies.get("user_id"))
        response = ResponseApiServers(user_id=user_id, password=password, ip=ip)
        return await response.post_add_server()
    except Exception as e:
        return f"Error: {e}"


@router.post('/servers/{user_id}/{server_id}')
async def check_server(user_id: int, server_id: int):
    response = ResponseApiServers(user_id=user_id, server_id=server_id)
    return await response.check_server()


@router.delete('/servers/{user_id}/{server_id}')
async def remove_server(user_id: int, server_id: int):
    response = ResponseApiServers(user_id=user_id, server_id=server_id)
    return await response.remove_server()


@router.get('/servers/{user_id}/{server_id}', response_class=HTMLResponse)
async def info_server(user_id: int, server_id: int, request: Request):
    try:
        current_user_id = int(request.cookies.get("user_id"))
        response = ResponseApiServers(
            user_id=user_id,
            server_id=server_id,
            current_user_id=current_user_id)
    except Exception as e:
        return f"Error: {e}"

    return await response.info_server(request)
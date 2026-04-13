import asyncio
from os import getenv
from typing import Annotated

from dotenv import load_dotenv
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from api.routes.login import add_cookie_user_login, verify_telegram_data
from repositories.server_repository import (
    create_server,
    get_server_by_id,
    have_user_server,
    list_user_connected_servers,
    remove_server_by_id,
)
from services.server_check import result_check_server

templates = Jinja2Templates(directory="api/templates")
router = APIRouter()

load_dotenv()

telegram_bot_login = (getenv("BOT_LOGIN"))


@router.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
    name='index.html',
    request=request,
    context={'telegram_bot_login': telegram_bot_login}
    )


@router.post('/login')
async def login(user: dict, response: Response):
    result = await verify_telegram_data(user)
    if result:
        user_id = user.get('id')
        await add_cookie_user_login(user_id=user_id, response=response)
        return {'status': 'ok', "user": user.get('first_name')}
    response.status_code = 401
    return {'status': 'Error', 'message': 'Invalid data'}


@router.get('/main_menu', response_class=HTMLResponse)
async def main_menu(request: Request):
    return templates.TemplateResponse(name='main_menu.html',
                                      request=request)


@router.get('/servers', response_class=HTMLResponse)
async def servers(request: Request):
    user_id = int(request.cookies.get("user_id"))
    servers = await list_user_connected_servers(user_id)
    flash = request.cookies.get("flash")
    return templates.TemplateResponse(
        name='servers.html',
        request=request,
        context={'servers': servers, 'user_id': user_id, 'flash': flash}
    )


@router.get('/servers/add')
async def get_add_server(request: Request):
    flash = request.cookies.get("flash")
    response = templates.TemplateResponse(
        name='add_server.html', request=request, context={'flash': flash})
    response.delete_cookie('flash')
    return response


@router.post('/servers/add')
async def post_add_server(
        request: Request,
        password: Annotated[str, Form()],
        ip: Annotated[str, Form()]
    ):

    user_id = int(request.cookies.get("user_id"))
    result_validate_server = await have_user_server(
        user_id=user_id,
        server_ip=ip
    )
    if result_validate_server == "valid_ip":
        await create_server(user_id=user_id, password=password, ip=ip)
        response = RedirectResponse(url='/servers', status_code=303)
        response.set_cookie("flash", "Server added successfully")
        return response
    elif result_validate_server == "invalid_ip":
        response = RedirectResponse(url='/servers/add', status_code=303)
        response.set_cookie("flash", "Invalid ip")
        return response
    else:
        response = RedirectResponse(url='/servers/add', status_code=303)
        response.set_cookie("flash", "Server in your list")
        return response


@router.post('/servers/{user_id}/{server_id}')
async def check_server(user_id: int, server_id: int):
    server = await get_server_by_id(server_id)
    if server:
        task = asyncio.create_task(result_check_server(server=server))
        await task
        return RedirectResponse(
            url=f'/servers/{user_id}/{server_id}',
            status_code=303
        )
    return {'status': 'Error', 'message': 'Invalid data'}


@router.delete('/servers/{user_id}/{server_id}')
async def remove_server(user_id: int, server_id: int):
    await remove_server_by_id(server_id)
    return RedirectResponse(url='/servers', status_code=303)


@router.get('/servers/{user_id}/{server_id}', response_class=HTMLResponse)
async def info_server(user_id: int, server_id: int, request: Request):
    server = await get_server_by_id(server_id)
    return templates.TemplateResponse(
        name='info_server.html',
        request=request,
        context={'user_id': user_id, 'server': server}
    )
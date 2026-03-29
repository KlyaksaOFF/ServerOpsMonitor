from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

from .login import add_cookie_user_login, verify_telegram_data

templates = Jinja2Templates(directory="api/templates")
router = APIRouter()


@router.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(name='index.html',
                                      request=request)


@router.post('/login')
async def login(user: dict, response: Response):
    result = await verify_telegram_data(user)
    if result:
        await add_cookie_user_login(user_id=user.get('id'), response=response)
        return {'status': 'ok', "user": user['first_name']}
    response.status_code = 401
    return {'status': 'Error', 'message': 'Invalid data'}


@router.get('/main_menu', response_class=HTMLResponse)
async def main_menu(request: Request):
    return templates.TemplateResponse(name='main_menu.html',
                                      request=request)


@router.get('/servers', response_class=HTMLResponse)
async def servers(request: Request):
    return templates.TemplateResponse(name='servers.html',
                                      request=request)

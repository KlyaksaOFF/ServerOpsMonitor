from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="api/templates")
router = APIRouter()


@router.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(name='index.html',
                                      request=request)


@router.post('/login', response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(name='login.html',
                                      request=request)


@router.get('/main_menu', response_class=HTMLResponse)
async def main_menu(request: Request):
    return templates.TemplateResponse(name='main_menu.html',
                                      request=request)


@router.get('/servers', response_class=HTMLResponse)
async def servers(request: Request):
    return templates.TemplateResponse(name='servers.html',
                                      request=request)

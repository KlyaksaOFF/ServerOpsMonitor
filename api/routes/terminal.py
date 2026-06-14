from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="api/templates/terminal")


@router.get('/terminal', response_class=HTMLResponse)
async def index_connect_terminal(request: Request):
    return templates.TemplateResponse(
        name='terminal_index.html',
        request=request,
        context={})


@router.post('/terminal')
async def connect_terminal(
        request: Request,
        ip: Annotated[str, Form()],
        root: Annotated[str, Form()],
        password: Annotated[str, Form()]):

    return templates.TemplateResponse(
        name='terminal.h tml',
        request=request,
        context={})


@router.get('/terminal/online', response_class=HTMLResponse)
async def online_terminal(request: Request):
    return templates.TemplateResponse(
    name='terminal_web.html',
    request=request,
    context={})
from typing import Annotated

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="api/templates/terminal")


@router.get('/terminal', response_class=HTMLResponse)
async def index_connect_terminal(request: Request):
    return templates.TemplateResponse(
        name='terminal_index.html',
        request=request,
        context={})


@router.post('/connect_terminal')
async def connect_terminal(
        request: Request,
        ip: Annotated[str, Form()],
        root: Annotated[str, Form()],
        password: Annotated[str, Form()]):
    return templates.TemplateResponse(
        name='web_terminal_online.html',
        request=request,
        context={})

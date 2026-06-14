
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="api/templates/terminal")


@router.get('/terminal', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        name='terminal_index.html',
        request=request,
        context={})

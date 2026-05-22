from typing import Annotated

import requests
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="api/templates")


@router.get('/checkurl/', response_class=HTMLResponse)
async def checkurl_main(request: Request):
    response = templates.TemplateResponse(
        name='check_url.html', request=request)
    return response


@router.post('/checkurl/', response_class=HTMLResponse)
async def checkurl_result(request: Request, url: Annotated[str, Form()]):
    r = requests.get(url)

    response = templates.TemplateResponse(
        name='check_url.html', request=request, context={
            'status': r.status_code,
            'encoding': r.encoding,
            'headers': r.headers,
        })
    return response
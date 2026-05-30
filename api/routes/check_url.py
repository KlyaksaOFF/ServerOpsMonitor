import asyncio
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
    runner = await asyncio.to_thread(requests.get, url)
    response = templates.TemplateResponse(
        name='check_url.html', request=request, context={
            'status': runner.status_code,
            'encoding': runner.encoding,
            'headers': runner.headers,
        })
    return response
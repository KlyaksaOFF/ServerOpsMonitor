from os import getenv
from typing import Annotated

import ipinfo
from dotenv import load_dotenv
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="api/templates")
token = getenv("IPINFO_TOKEN")
load_dotenv()


@router.get('/ip/', response_class=HTMLResponse)
async def ip_main(request: Request):
    client_host = request.client.host
    response = templates.TemplateResponse(
        name='check_ip.html', request=request, context={'user_ip': client_host})
    return response


@router.post('/ip/', response_class=HTMLResponse)
async def check_ip(request: Request, ip_address: Annotated[str, Form()]):
    try:
        handler = ipinfo.getHandler(token)
        details = handler.getDetails(ip_address)
        result_data = {
            'ip': ip_address,
            'org': details.org,
            'country': details.country_name,
            'city': details.city
        }

        response = templates.TemplateResponse(
            name='check_ip.html',
            request=request,
            context={'result_data': result_data})
        return response
    except Exception:
        return HTMLResponse('Too many requests')
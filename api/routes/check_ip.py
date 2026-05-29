import asyncio
from os import getenv
from typing import Annotated

import ipinfo
from dotenv import load_dotenv
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from requests.exceptions import RequestException, Timeout

from utils.utils_validate_ip import ValidateIP

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
    validate_ip = ValidateIP(ip=ip_address).validate()
    try:
        if not validate_ip:
            raise ValueError

        handler = ipinfo.getHandler(token)
        runner = await asyncio.to_thread(handler.getDetails, ip_address)
        result_data = {
            'ip': ip_address,
            'org': runner.org,
            'country': runner.country_name,
            'city': runner.city
        }
        response = templates.TemplateResponse(
            name='check_ip.html',
            request=request,
            context={'result_data': result_data})
        return response

    except Timeout:
        error = 'Error: Timeout request to api, try again.'
        response = templates.TemplateResponse(
            name='check_ip.html',
            request=request,
            context={'error': error})
        return response

    except RequestException:
        error = 'Error: API request failed.'
        response = templates.TemplateResponse(
            name='check_ip.html',
            request=request,
            context={'error': error})
        return response

    except (ValueError, TypeError):
        error = 'Error: ValueError or TypeError.'
        response = templates.TemplateResponse(
            name='check_ip.html',
            request=request,
            context={'error': error})
        return response
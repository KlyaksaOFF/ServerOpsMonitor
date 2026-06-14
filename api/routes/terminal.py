import asyncio
from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from services.server_api_terminal import (
    clean_terminal_output,
    connect_ssh_to_server,
    read_output,
    send_remote_command_terminal,
)

router = APIRouter()
templates = Jinja2Templates(directory="api/templates/terminal")

active_session = {}


@router.get('/terminal', response_class=HTMLResponse)
async def index_connect_terminal(request: Request):
    return templates.TemplateResponse(
        name='terminal.html',
        request=request,
        context={'auth': False})


@router.post('/terminal')
async def connect_terminal(
        request: Request,
        ip: Annotated[str, Form()],
        user: Annotated[str, Form()],
        password: Annotated[str, Form()]):

    channel = await connect_ssh_to_server(ip, user, password)
    active_session['ip'] = ip
    active_session['user'] = user
    active_session['password'] = password
    active_session['channel'] = channel

    output = await asyncio.to_thread(read_output, channel)
    result = clean_terminal_output(output)
    return templates.TemplateResponse(
        name='terminal.html',
        request=request,
        context={
            'auth': True,
            'user': user,
            'result': result
        }
    )


@router.post('/terminal/command')
async def command_terminal(
        request: Request,
        command: Annotated[str, Form()]):

    channel = active_session.get('channel')

    if channel is None:
        return templates.TemplateResponse(
            name='terminal.html',
            request=request,
            context={
                'auth': False,
                'result': 'Not connected'
            })

    send_remote_command_terminal(channel, "ls --color=never")

    await asyncio.sleep(0.5)

    output = await asyncio.to_thread(read_output, channel)
    result = clean_terminal_output(output)

    return templates.TemplateResponse(
        name='terminal.html',
        request=request,
        context={
    'auth': True,
    'user': active_session['user'],
    'command': command,
    'result': result})
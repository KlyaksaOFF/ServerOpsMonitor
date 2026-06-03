import asyncio
from os import getenv

from dotenv import load_dotenv
from fastapi import Request
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from api.routes.login import add_cookie_user_login, verify_telegram_data
from repositories.RequestToRepository import RequestToRepository
from services.server_check import result_check_server
from utils.utils_validate_ip import ProcessCreateServer

load_dotenv()

templates_servers = Jinja2Templates(directory="api/templates/servers")
templates_main = Jinja2Templates(directory="api/templates")
telegram_bot_login = (getenv("BOT_LOGIN"))


class ResponseApiServers(RequestToRepository):
    def __init__(self,
                 user_id=None,
                 server_id=None,
                 password=None,
                 ip=None,
                 current_user_id=None):

        self.user_id = user_id
        self.server_id = server_id
        self.password = password
        self.ip = ip
        self.current_user_id = current_user_id

    @staticmethod
    async def index(request: Request):
        return templates_main.TemplateResponse(
            name='auth.html',
            request=request,
            context={'telegram_bot_login': telegram_bot_login})

    @staticmethod
    async def login(response: Response, user):
        result_verify = await verify_telegram_data(user)
        if result_verify:
            user_id = user.get('id')
            await add_cookie_user_login(user_id=user_id, response=response)
            return {'status': 'ok', "user": user.get('first_name')}
        response.status_code = 401
        return {'status': 'Error', 'message': 'Invalid data'}

    @staticmethod
    async def main_menu(request: Request):
        return templates_main.TemplateResponse(name='index.html',
                                          request=request)

    async def servers(self, request: Request):
        list_servers_user = await self.list_con_servers(user_id=self.user_id)
        flash = request.cookies.get("flash")
        response = templates_servers.TemplateResponse(
            name='servers.html',
            request=request,
            context={
            'servers': list_servers_user,
            'user_id': self.user_id,
            'flash': flash})
        response.delete_cookie('flash')
        return response

    @staticmethod
    async def get_add_server(request: Request):
        flash = request.cookies.get("flash")
        response = templates_servers.TemplateResponse(
            name='add_server.html', request=request, context={'flash': flash})
        response.delete_cookie('flash')
        return response

    async def post_add_server(self):
        response = ProcessCreateServer(
            user_id=self.user_id,
            password=self.password,
            ip=self.ip)
        return await response.validate_and_create_server()

    async def check_server(self):
        server = await self.get_server(server_id=self.server_id)
        if server:
            task = asyncio.create_task(result_check_server(server=server))
            await task
            return RedirectResponse(
                url=f'/servers/{self.user_id}/{self.server_id}',
                status_code=303)
        return {'status': 'Error', 'message': 'Invalid data'}

    async def remove_server(self):
        await self.remove_server_by_server_id(self.server_id)
        return RedirectResponse(url='/servers', status_code=303)

    async def info_server(self, request: Request):
        server = await self.get_server(self.server_id)
        return templates_servers.TemplateResponse(
        name='info_server.html',
        request=request,
        context={
        'user_id': self.user_id,
        'server': server,
        'current_user_id': self.current_user_id})
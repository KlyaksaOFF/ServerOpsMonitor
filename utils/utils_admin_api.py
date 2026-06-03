
from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repositories.admins import (
    add_new_admin,
    all_admin_users,
    check_admin_user_id,
    remove_user_admin,
)
from repositories.server_repository import (
    all_servers_ip,
    all_users_id,
    count_unique_servers,
    count_unique_users,
    remove_all_where_ip,
)

templates = Jinja2Templates(directory="api/templates/admins")


class ResultResponseAndRepository:
    def __init__(self, user_id):
        self.user_have_admin = None
        self.user_id = user_id

    async def result_check_user_from_admin(self):
        self.user_have_admin = await check_admin_user_id(self.user_id)
        return self.user_have_admin

    async def util_response_check_admin(self, request: Request):
        await self.result_check_user_from_admin()
        if self.user_have_admin:
            flash = request.cookies.get("flash")

            response = templates.TemplateResponse(
                name='admin.html',
                request=request,
                context={
                    'user_have_admin': self.user_have_admin,
                    'count_unique_users': await count_unique_users(),
                    'count_unique_servers': await count_unique_servers(),
                    'all_unique_users_id': await all_users_id(),
                    'all_unique_servers_ip': await all_servers_ip(),
                    'flash': flash
                })

            response.delete_cookie('flash')
            return response

        response = RedirectResponse(
            url='/servers/', status_code=303)
        response.set_cookie("flash", "You don't have permission!")
        return response

    async def util_response_permission_menu(self, request: Request):
        await self.result_check_user_from_admin()
        if self.user_have_admin:
            flash = request.cookies.get("flash")
            admin_users = await all_admin_users()

            response = templates.TemplateResponse(
                name='permission_menu.html',
                request=request,
                context={'flash': flash, 'admins': admin_users})

            response.delete_cookie('flash')
            return response

        response = RedirectResponse(
            url='/servers/', status_code=303)
        response.set_cookie("flash", "You don't have permission!")
        return response

    async def util_response_permission_menu_add_new_admin(self,
            current_user_id,
            new_admin_id):

        await self.result_check_user_from_admin()
        if self.user_have_admin:
            try:
                result_add = await add_new_admin(
                    current_admin_id=current_user_id,
                    new_admin_id=int(new_admin_id),
                )
                match result_add:
                    case True:
                        response = RedirectResponse(url='/admin/',
                                                    status_code=303)
                        response.set_cookie("flash", "New admin added")
                        return response
                    case False:
                        response = RedirectResponse(
                            url='/admin/permission-menu/', status_code=303)
                        response.set_cookie("flash", "Fail operation")
                        return response
            except Exception as e:
                response = RedirectResponse(
                    url='/admin/permission-menu/', status_code=303)
                response.set_cookie("flash", f"Error: {e}")
                return response

        response = RedirectResponse(
            url='/servers/', status_code=303)
        response.set_cookie("flash", "You don't have permission!")
        return response

    async def util_response_remove_from_admins(self):
        await remove_user_admin(self.user_id)
        response = RedirectResponse(
            url='/admin/permission-menu/', status_code=303)
        response.set_cookie("flash", "Success! Admin removed")
        return response

    @staticmethod
    async def util_response_remove_all_ip(ip):
        await remove_all_where_ip(ip)
        response = RedirectResponse(url='/admin', status_code=303)
        return response
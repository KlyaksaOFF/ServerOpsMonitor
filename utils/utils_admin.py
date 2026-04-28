
from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repositories.server_repository import (
    add_new_admin,
    all_admin_users,
    all_servers_ip,
    all_users_id,
    count_unique_servers,
    count_unique_users,
)

templates = Jinja2Templates(directory="api/templates")


async def util_process_check_admin(request: Request, user_have_admin):
    if user_have_admin:
        count_value_unique_users = await count_unique_users()
        count_value_unique_servers = await count_unique_servers()
        all_unique_users_id = await all_users_id()
        all_unique_servers_ip = await all_servers_ip()
        flash = request.cookies.get("flash")

        response = templates.TemplateResponse(
            name='admin.html',
            request=request,
            context={
                'user_have_admin': user_have_admin,
                'count_unique_users': count_value_unique_users,
                'count_unique_servers': count_value_unique_servers,
                'all_unique_users_id': all_unique_users_id,
                'all_unique_servers_ip': all_unique_servers_ip,
                'flash': flash
            })

        response.delete_cookie('flash')
        return response

    else:
        response = RedirectResponse(
            url='/servers/', status_code=303)
        response.set_cookie("flash", "You don't have permission!")
        return response


async def util_process_permission_menu(request: Request, result_check):
    if result_check:
        flash = request.cookies.get("flash")
        admin_users = await all_admin_users()

        response = templates.TemplateResponse(
        name='permission_menu.html',
        request=request,
        context={'flash': flash, 'admins': admin_users})

        response.delete_cookie('flash')
        return response
    else:
        response = RedirectResponse(
        url='/servers/', status_code=303)
        response.set_cookie("flash", "You don't have permission!")
        return response


async def util_process_permission_menu_add_new_admin(
        result_check,
        current_user_id,
        new_admin_id):

    if result_check:
        try:
            result_add = await add_new_admin(
            current_admin_id=current_user_id,
            new_admin_id=int(new_admin_id),
            )

            match result_add:
                case True:
                    response = RedirectResponse(url='/admin/', status_code=303)
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
    else:
        response = RedirectResponse(
        url='/servers/', status_code=303)
        response.set_cookie("flash", "You don't have permission!")
        return response


async def util_process_remove_from_admins():
    response = RedirectResponse(
    url='/admin/permission-menu/', status_code=303
    )
    response.set_cookie("flash", "Success! Admin removed")
    return response
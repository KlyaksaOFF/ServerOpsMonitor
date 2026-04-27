from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from repositories.server_repository import (
    add_new_admin,
    all_admin_users,
    all_servers_ip,
    all_users_id,
    check_admin_user_id,
    count_unique_servers,
    count_unique_users,
    remove_all_where_ip,
    remove_user_admin,
)

router = APIRouter()

templates = Jinja2Templates(directory="api/templates")

@router.get('/admin/', response_class=HTMLResponse)
async def admin_main(request: Request):
    current_user_id = int(request.cookies.get("user_id"))

    user_have_admin = await check_admin_user_id(current_user_id)

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


@router.delete('/admin/{server_ip}/delete-all')
async def admin_delete_ip(server_ip):
    await remove_all_where_ip(server_ip)
    return RedirectResponse(url='/admin', status_code=303)


@router.get('/admin/permission-menu/')
async def permission_menu(request: Request):
    current_user_id = int(request.cookies.get("user_id"))
    result_check = await check_admin_user_id(current_user_id)

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


@router.post('/admin/permission-menu/')
async def permission_menu_add_new_admin(
        request: Request, new_admin_id: Annotated[str, Form()]
):

    current_user_id = int(request.cookies.get("user_id"))
    result_check = await check_admin_user_id(current_user_id)
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


@router.delete('/admin/permission-menu/{user_id}')
async def remove_from_admin(user_id):
    await remove_user_admin(int(user_id))

    response = RedirectResponse(
    url='/admin/permission-menu/', status_code=303
    )
    response.set_cookie("flash", "Success! Admin removed")
    return response
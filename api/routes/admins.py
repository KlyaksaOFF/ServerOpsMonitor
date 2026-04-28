from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from repositories.server_repository import (
    check_admin_user_id,
    remove_all_where_ip,
    remove_user_admin,
)
from utils.utils_admin import (
    util_process_check_admin,
    util_process_permission_menu,
    util_process_permission_menu_add_new_admin,
    util_process_remove_from_admins,
)

router = APIRouter()

templates = Jinja2Templates(directory="api/templates")


@router.get('/admin/', response_class=HTMLResponse)
async def admin_main(request: Request):
    current_user_id = int(request.cookies.get("user_id"))
    user_have_admin = await check_admin_user_id(current_user_id)
    return await util_process_check_admin(
        request=request, user_have_admin=user_have_admin)


@router.delete('/admin/{server_ip}/delete-all')
async def admin_delete_ip(server_ip):
    await remove_all_where_ip(server_ip)
    return RedirectResponse(url='/admin', status_code=303)


@router.get('/admin/permission-menu/')
async def permission_menu(request: Request):
    current_user_id = int(request.cookies.get("user_id"))
    result_check_user_admin = await check_admin_user_id(current_user_id)
    return await util_process_permission_menu(
        request=request, result_check=result_check_user_admin)


@router.post('/admin/permission-menu/')
async def permission_menu_add_new_admin(
        request: Request,
        new_admin_id: Annotated[str, Form()]):

    current_user_id = int(request.cookies.get("user_id"))
    result_check_user_admin = await check_admin_user_id(current_user_id)
    return await util_process_permission_menu_add_new_admin(
        result_check=result_check_user_admin,
        current_user_id=current_user_id,
        new_admin_id=new_admin_id)


@router.delete('/admin/permission-menu/{user_id}')
async def remove_from_admins(user_id):
    await remove_user_admin(int(user_id))
    return await util_process_remove_from_admins()
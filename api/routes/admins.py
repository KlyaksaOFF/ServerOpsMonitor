from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from utils.utils_admin import (
    ResultResponseAndRepository,
)

router = APIRouter()

templates = Jinja2Templates(directory="api/templates")


@router.get('/admin/', response_class=HTMLResponse)
async def admin_main(request: Request):
    current_user_id = int(request.cookies.get("user_id"))
    response = ResultResponseAndRepository(user_id=current_user_id)
    return await response.util_response_check_admin(request=request)


@router.delete('/admin/{ip}/delete-all')
async def admin_delete_ip(ip):
    response = ResultResponseAndRepository(user_id=None)
    return await response.util_response_remove_all_ip(ip=ip)

@router.get('/admin/permission-menu/')
async def permission_menu(request: Request):
    current_user_id = int(request.cookies.get("user_id"))
    response = ResultResponseAndRepository(user_id=current_user_id)
    return await response.util_response_permission_menu(request=request)


@router.post('/admin/permission-menu/')
async def permission_menu_add_new_admin(
        request: Request,
        new_admin_id: Annotated[str, Form()]):

    current_user_id = int(request.cookies.get("user_id"))
    response = ResultResponseAndRepository(user_id=current_user_id)
    return await response.util_response_permission_menu_add_new_admin(
        current_user_id=current_user_id,
        new_admin_id=new_admin_id)


@router.delete('/admin/permission-menu/{user_id}')
async def remove_from_admins(user_id):
    response = ResultResponseAndRepository(user_id=int(user_id))
    return await response.util_response_remove_from_admins()
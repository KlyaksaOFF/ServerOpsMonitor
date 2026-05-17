import logging

from aiogram.fsm.context import FSMContext
from fastapi.responses import RedirectResponse

from handlers.fsm_states import AddServer
from repositories.server_repository import create_server


class ValidateIP:
    def __init__(self, ip):
        self.ip = ip

    def validate(self):
        parts_ip = self.ip.split('.')
        for part in parts_ip:
            if not part.isdigit():
                return False
            if not 0 <= int(part) <= 255:
                return False

        result_validate_ip = (
                len(self.ip) > 0
                and len(parts_ip) == 4
        )
        return result_validate_ip


async def validate_result_ip_telegram(server_ip, user_id, state: FSMContext):
    from repositories.server_repository import check_user_have_server_ip

    server = await check_user_have_server_ip(
        user_id=user_id,
        server_ip=server_ip
    )

    if not server:
        validate_ip = ValidateIP(server_ip)
        if validate_ip.validate():
            await state.update_data(ip=server_ip)
            await state.set_state(AddServer.waiting_for_password)
            logging.info('Input valid ip')
            return 'valid_ip'
        else:
            logging.info('Input invalid ip')
            return 'invalid_ip'

    logging.info('Server in db')
    return 'ip_in_db'


async def validate_result_ip_api(user_id, ip):
    from repositories.server_repository import check_user_have_server_ip

    server = await check_user_have_server_ip(
        user_id=user_id,
        server_ip=ip
    )

    if not server:
        validate_ip = ValidateIP(ip)
        if validate_ip.validate():
            logging.info('Input valid ip')
            return 'valid_ip'
        else:
            logging.info('Input invalid ip')
            return 'invalid_ip'

    logging.info('Server in db')
    return 'ip_in_db'


class ProcessCreateServer:
    def __init__(self, user_id, password, ip):
        self.user_id = user_id
        self.password = password
        self.ip = ip

    async def validate_and_create_server(self):

        result_validate_server = \
            await validate_result_ip_api(
            self.user_id,
            self.ip
        )

        match result_validate_server:

            case "valid_ip":
                await create_server(
                    user_id=self.user_id,
                    password=self.password,
                    ip=self.ip)
                response = RedirectResponse(url='/servers', status_code=303)
                response.set_cookie("flash", "Server added successfully")
                return response
            case "invalid_ip":
                response = RedirectResponse(url='/servers/add', status_code=303)
                response.set_cookie("flash", "Invalid ip")
                return response
            case _:
                response = RedirectResponse(url='/servers/add', status_code=303)
                response.set_cookie("flash", "Server in your list")
                return response
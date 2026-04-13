import logging

from aiogram.fsm.context import FSMContext

from handlers.fsm_states import AddServer


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
        result_validate_ip = (len(self.ip) > 0
                              and len(parts_ip) == 4)
        return result_validate_ip


async def result_ip_telegram(server, server_ip, state: FSMContext):
    if not server:
        validate_ip = ValidateIP(server_ip)
        if validate_ip.validate():
            await state.update_data(ip=server_ip)
            await state.set_state(AddServer.waiting_for_password)
            return 'valid_ip'
        else:
            return 'invalid_ip'
    # if server in db (telegram checking)
    logging.info('Server in db')
    return 'ip_in_db'


async def result_ip_api(server, server_ip):
    if not server:
        validate_ip = ValidateIP(server_ip)
        if validate_ip.validate():
            return 'valid_ip'
        else:
            return 'invalid_ip'
    # if server in db (web checking)
    logging.info('Server in db')
    return 'ip_in_db'
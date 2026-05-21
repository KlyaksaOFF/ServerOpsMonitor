import logging

from repositories.RequestToRepository import RequestToRepository
from texts.texts import (
    ERROR_FORMAT_IP,
    ERROR_INVALID_IP,
    SEND_PASSWORD,
    SERVER_IN_YOUR_LIST,
)
from utils.utils_validate_ip import validate_result_ip_telegram


class ResponseBotServers(RequestToRepository):
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

    async def process_password(self):
        await self.create_server(
            ip=self.ip,
            user_id=self.user_id,
            password=self.password)

        logging.info('Server created')

    async def get_server(self):
        return await self.get_server_by_id(self.server_id)

    async def remove_server(self):
        return await self.remove_server_by_server_id(self.server_id)

    async def autocheck_process(self):
        return await self.process_function_autocheck(self.server_id)

    async def autocheck_state(self):
        return await self.state_autocheck_server(self.server_id)

    async def process_ip(self, state=None, message=None):
        try:
            result_validate_server = await validate_result_ip_telegram(
                server_ip=self.ip,
                user_id=self.user_id,
                state=state
            )
            if result_validate_server == "valid_ip":
                return await message.answer(SEND_PASSWORD)
            elif result_validate_server == "invalid_ip":
                return await message.answer(ERROR_INVALID_IP)
            else:
                return await message.answer(SERVER_IN_YOUR_LIST)
        except AttributeError:
            return await message.answer(ERROR_FORMAT_IP)
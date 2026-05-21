from repositories.server_repository import (
    create_server,
    get_server_by_id,
    list_user_connected_servers,
    process_function_autocheck,
    remove_server_by_server_id,
    state_autocheck_server,
)


class RequestToRepository:
    @staticmethod
    async def get_server_by_id(server_id: int):
        return await get_server_by_id(server_id=server_id)

    @staticmethod
    async def create_server(ip, password, user_id: int):
        return await create_server(user_id=user_id, ip=ip, password=password)

    @staticmethod
    async def process_function_autocheck(server_id: int):
        return await process_function_autocheck(server_id=server_id)

    @staticmethod
    async def state_autocheck_server(server_id: int):
        return await state_autocheck_server(server_id=server_id)

    @staticmethod
    async def remove_server_by_server_id(server_id: int):
        return await remove_server_by_server_id(server_id=server_id)

    @staticmethod
    async def get_server(server_id: int):
        return await get_server_by_id(server_id=server_id)

    @staticmethod
    async def list_con_servers(user_id: int):
        return await list_user_connected_servers(user_id=user_id)

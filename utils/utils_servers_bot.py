from repositories.server_repository import (
    create_server,
    get_server_by_id,
    process_function_autocheck,
    remove_server_by_server_id,
    state_autocheck_server,
)

class RequestToRepository:
    pass

class ResponseBotServers(RequestToRepository):
    pass
import asyncio

from ansible_runner import run

from repositories.server_repository import added_check_in_table_server


async def check_server(server):
    runner_args = {
        'inventory': server.ip,
        'passwords': {'password': server.password},
        'extravars': {'ansible_user': 'root',
                   'ansible_ssh_pass': server.password,
                   'ansible_ssh_extra_args':
                       '-o PubkeyAuthentication=no '
                       '-o PreferredAuthentications=password'},
        'playbook': [{
            'hosts': 'all',
            'gather_facts': False,
            'tasks': [
                {'name': 'ping test', 'ping': None},
                {'name': 'uptime server', 'command': 'uptime'}
            ]
        }]
    }

    runner = await asyncio.to_thread(run, **runner_args)

    return runner


def take_data_check_server(runner):
    result_check = {"status": runner.status}
    for event in runner.events:
        event_data = event.get('event_data')
        if event.get('event') == 'runner_on_ok':
            task_name = event_data.get('task')
            res = event_data.get('res')

            if task_name == 'ping test':
                result_check['ping'] = res.get('ping')

            elif task_name == 'uptime server':
                result_check['uptime'] = res.get('stdout')
    return result_check


async def result_check_server(server):
    runner = await check_server(server)
    result_check = take_data_check_server(runner=runner)
    uptime = result_check.get('uptime')
    ping = result_check.get('ping')
    status = result_check.get('status')
    code = runner.rc
    await added_check_in_table_server(server, ping, uptime)
    return (
        f"✅ {server.ip} \n\n"
        f"Ping: {ping} \n"
        f"Uptime: {uptime}\n"
        f"Code: {code}\n"
        f"Status: {status}"
        if code == 0 else f"Code error: {code} \n"
                               f"Status: {status}"
    )
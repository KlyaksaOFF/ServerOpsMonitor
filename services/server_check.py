import asyncio

from ansible_runner import run

from repositories.server_repository import added_check_in_table_server


async def check_server(server):
    runner_args = {
        'inventory': f"{server.ip}",
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
                {'name': 'uptime server', 'command': 'uptime'},
            ]
        }]
    }

    runner = await asyncio.to_thread(run, **runner_args)

    return runner


def take_data_check_server(runner):
    result_check = {"status": runner.status}
    for event in runner.events:
        if not event:
            continue

        event_data = event.get('event_data') or {}
        event_name = event.get('event')
        res = event_data.get('res') or {}

        if event_name in ('runner_on_failed', 'runner_on_unreachable'):
            result_check['msg'] = res.get('msg')

        task_name = event_data.get('task')

        match task_name:
            case 'ping test':
                result_check['ping'] = res.get('ping')
            case 'uptime server':
                result_check['uptime'] = res.get('stdout')

    return result_check


async def result_check_server(server):
    runner = await check_server(server)
    result_check = take_data_check_server(runner=runner)
    uptime = result_check.get('uptime')
    ping = result_check.get('ping')
    status = result_check.get('status')
    msg = result_check.get('msg')
    code = runner.rc
    await added_check_in_table_server(
        server=server,
        ping=ping,
        uptime=uptime,
        msg=msg
    )

    return (
        "CHECK SERVER: \n\n"
        f"✅ {server.ip} \n\n"
        f"Ping: {ping} \n"
        f"Uptime: {uptime}\n"
        f"Code: {code}\n"
        f"Status: {status} \n"
        if code == 0 else
        "CHECK SERVER: \n\n"
        f"❌ {server.ip} \n\n"
        f"Code error: {code} \n"
        f"Status: {status} \n"
        f"Msg: {msg}"
    )
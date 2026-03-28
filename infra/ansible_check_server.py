import asyncio

from ansible_runner import run_async


async def check_server(server):
    thread, runner = run_async(
        inventory=server.ip,
        passwords={'password': server.password},
        extravars={'ansible_user': 'root',
                   'ansible_ssh_pass': server.password,
                   'ansible_ssh_extra_args':
                       '-o PubkeyAuthentication=no '
                       '-o PreferredAuthentications=password'},
        playbook=[{'hosts': 'all', 'gather_facts': False, 'tasks':
                       [{'name': 'ping test', 'ping': None},
                        {'name': 'uptime server', 'command': 'uptime'}]}]
    )

    while thread.is_alive():
        await asyncio.sleep(0.1)

    return runner


def take_data_check_server(runner):
    result_check_server = {}
    for event in runner.events:
        event_data = event.get('event_data')
        if event.get('event') == 'runner_on_ok':
            task_name = event_data.get('task')
            res = event_data.get('res')

            if task_name == 'ping test':
                result_check_server['ping'] = res.get('ping')

            elif task_name == 'uptime server':
                result_check_server['uptime'] = res.get('stdout')
    return result_check_server


def result_check_server(server, runner):
    result_check_server = take_data_check_server(runner=runner)
    return (
        f"✅ {server.ip} \n\n"
        f"Ping: {result_check_server['ping']} \n"
        f"Uptime: {result_check_server['uptime']}"
        if runner.rc == 0 else "Error"
    )
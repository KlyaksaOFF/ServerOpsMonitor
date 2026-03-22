from ansible_runner import run_async
import asyncio

async def ping_server(server):
    thread, runner = run_async(
        inventory=server.ip,
        passwords={'password': server.password},
        extravars={'ansible_user': 'root', 'ansible_ssh_pass': server.password,
                   'ansible_ssh_extra_args': '-o PubkeyAuthentication=no -o PreferredAuthentications=password'},
        playbook=[{'hosts': 'all', 'gather_facts': False, 'tasks': [{'name': 'ping test', 'ping': None}, {'name': 'uptime server', 'command': 'uptime'}]}]
    )

    while thread.is_alive():
        await asyncio.sleep(0.1)

    return runner


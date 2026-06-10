import asyncio

from ansible_runner import run

from utils.utils_password__encryption import EncryptionPassword


async def update_server(server):
    decrypted_password = EncryptionPassword().decode(server.password)
    runner_args = {
        'inventory': server.ip,
        'passwords': {'password': decrypted_password},
        'extravars': {'ansible_user': 'root',
                   'ansible_ssh_pass': decrypted_password,
                   'ansible_ssh_extra_args':
                       '-o PubkeyAuthentication=no '
                       '-o PreferredAuthentications=password'},
        'playbook': [{
            'hosts': 'all',
            'gather_facts': False,
            'tasks': [
                {'name': 'apt update', 'command': 'sudo apt update'},
            ]
        }]
    }

    runner = await asyncio.to_thread(run, **runner_args)

    return runner


async def result_update_server(server):
    runner = await update_server(server)

    code = runner.rc
    status = runner.status
    return (
        f"UPDATE: \n\n"
        f"✅ {server.ip} \n\n"
        f"Code: {code}\n"
        f"Status: {status}"
        if code == 0 else
        f"UPDATE: \n\n"
        f"❌ {server.ip} \n\n"
        f"Code error: {code} \n"
        f"Status: {status}"
    )
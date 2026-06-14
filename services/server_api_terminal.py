import asyncio

import paramiko

def terminal(ip, user, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip, username=user, password=password)
    stdin, stdout, stderr = ssh.exec_command(command)
    result_terminal = stdout.read().decode()
    ssh.close()
    return result_terminal


async def result_thread_terminal(ip, user, password, command):
    output_thread_terminal = await asyncio.to_thread(terminal, ip, user, password, command)
    return output_thread_terminal


#result = asyncio.run(result_thread_terminal(ip, user, password, command))
# перенести в функцию, где будет показ терминала

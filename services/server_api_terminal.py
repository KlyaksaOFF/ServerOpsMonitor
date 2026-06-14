import asyncio

import paramiko

ip = '123'
user = 'root'
password = '123'
command = 'ps'
def connect_terminal(ip, user, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, username=user, password=password)
        channel = ssh.invoke_shell()
        return channel
    except Exception as error:
        return error


async def connect_ssh_to_server(ip, user, password):
    channel = await asyncio.to_thread(
        connect_terminal,
        ip,
        user,
        password)
    return channel


def send_remote_command_terminal(channel, command):
    channel.send(command + "\n")

def read_output(channel):
    while True:
        if channel.recv_ready():
            data = channel.recv(4096)
            return data.decode()
        return ""

async def output(ip, user, password):
    channel = await connect_ssh_to_server(ip, user, password)
    send_remote_command_terminal(channel, command='ps')
    await asyncio.sleep(0.5)
    output = await asyncio.to_thread(read_output, channel)
    return output

result = asyncio.run(output(ip, user, password))
print(result)
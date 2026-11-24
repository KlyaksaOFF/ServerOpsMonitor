import asyncio
import re

import paramiko


def connect_terminal(ip, user, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, username=user, password=password)
        channel = ssh.invoke_shell()
        return channel
    except Exception as error:
        raise error


async def connect_ssh_to_server(ip, user, password):
    channel = await asyncio.to_thread(
        connect_terminal,
        ip,
        user,
        password)
    return channel


def send_remote_command_terminal(channel, command):
    channel.send(f"{command}\n")
    b = channel.send(f"{command}\n")
    print(b)


def read_output(channel):
    buffer = b""
    print("Buffer ready:", channel.recv_ready())
    while channel.recv_ready():
        buffer += channel.recv(4096)
        print("Buffer:", repr(buffer))
    return buffer.decode()


async def output(ip, user, password):
    channel = await connect_ssh_to_server(ip, user, password)
    await asyncio.sleep(5)
    output = await asyncio.to_thread(read_output, channel)
    return output


def clean_terminal_output(text: str) -> str:
    osc_escape = re.compile(
        r'\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)'
    )

    ansi_escape = re.compile(
        r'\x1b(?:\[[0-?]*[ -/]*[@-~]|[@-Z\\-_])'
    )

    text = osc_escape.sub('', text)
    text = ansi_escape.sub('', text)

    return text
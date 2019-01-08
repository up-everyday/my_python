# -*- coding: utf-8 -*-
import paramiko
import time
import sys
import re
import json
import os
import threading
import _cffi_backend

def usage():
    """
    Usage of cts in command line
    """
    print('Usage: {0} <IP> <Port> <User> <Password> <timeout> <command_list_file>'.format(sys.argv[0]))
    print('    Example: {0} 135.242.107.233 22 ainet ainet1 300 install_cts_commands'.format(sys.argv[0]))
    sys.exit(1)


def heartBeat(timeout, breakEvent):
    heartCount = 0
    while heartCount < timeout:
        if breakEvent.isSet():
            break
        time.sleep(1)
        heartCount += 1
    if not breakEvent.isSet():
        print('Operation timeout, {0} seconds passed.'.format(timeout))


def sendAndReceive(ssh, command, expect, searchReg = None):
    ssh.send("{0}\n".format(command))
    time.sleep(1)
    buff = ''
    while not buff.endswith(expect):
        resp = ssh.recv(9999)
        try:
            respStr = resp.decode('latin-1')
        except UnicodeDecodeError:
            try:
                respStr = resp.decode('ascii')
            except UnicodeDecodeError:
                try:
                    respStr = resp.decode('utf-8')
                except UnicodeDecodeError:
                    respStr = ''
                    return ''
        buff += respStr
    if searchReg:
        if searchReg.search(buff):
            return True, buff
        else:
            return False, buff

    else:
        return True, buff

def remote_run(IP, Port, User, Password, breakEvent, successEvent, command_list):
    ssh = None
    channel = None
    root_ps = 'SSH_TEMP_ROOT# '
    user_ps = 'SSH_TEMP_USER@ '

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=IP, port=Port, username=User, password=Password, timeout = 10, allow_agent=False,look_for_keys=False)
        try:
            channel = ssh.invoke_shell()
            if User != 'root':
                #switch to root
                sendAndReceive(channel, "su -", "Password: ")
                sendAndReceive(channel, "r00t", "root-# ")
            sendAndReceive(channel, 'export PS1="{0}"'.format(root_ps), root_ps)
            for commands in command_list:
                if not isinstance(commands, dict):
                    continue

                command = commands.get('command', '')
                expect = commands.get('expect', root_ps)
                if not command:
                    continue

                flag, result = sendAndReceive(channel, command, expect)

            successEvent.set()
        except Exception as e:
            print('Error appear when do ssh operation: {0}'.format(e))
        finally:
            if channel:
                channel.close()
    except Exception as e:
        print('SSH connect server failed: {0}'.format(e))
    finally:
        if ssh:
            ssh.close()
        breakEvent.set()

if __name__ == '__main__':
    if len(sys.argv) != 7:
        usage()

    IP = str(sys.argv[1])
    Port = int(sys.argv[2])
    User = str(sys.argv[3])
    Password = str(sys.argv[4])
    timeout = int(sys.argv[5])
    command_file = str(sys.argv[6])
    command_list = []
    try:
        if not os.path.exists(command_file):
            print('command_list_file: {0} not exist. exit!'.format(command_file))
            sys.exit(1)
        with open(command_file, 'r') as fio:
            command_list = json.loads(fio.read())
            if not isinstance(command_list, list):
                print('command_list_file: {0} format error, must be list. exit!'.format(command_file))
                sys.exit(1)
    except Exception as e:
        print('load command_list_file: {0} error: {1}'.format(command_file, e))

    if not command_list:
        print('No command need process, exit!')
        sys.exit(0)
    breakEvent = threading.Event()
    successEvent = threading.Event()
    restart_thread = threading.Thread(target=remote_run, args = (IP, Port, User, Password, breakEvent, successEvent, command_list, ))
    restart_thread.setDaemon(True)
    restart_thread.start()

    heart_thread = threading.Thread(target=heartBeat, args = (timeout, breakEvent,  ))
    heart_thread.start()
    heart_thread.join()

    if successEvent.isSet():
        sys.exit(0)
    else:
        sys.exit(1)



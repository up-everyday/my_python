# -*- coding:UTF-8 -*-
'''
基于用户名和密码实现 SSH远程登录，并在远程服务器上执行命令
'''
import paramiko
import sys
import time
import threading

def sendAndReceive(ssh, command, expect, searchReg = None):
    ssh.send("{0}\n".format(command))
    time.sleep(1)
    buff = ''
    print("###sendAndReceive expect is", expect)
    print("### buff.endswith(expect)", buff.endswith(expect))
    while not buff.endswith(expect):
        resp = ssh.recv(9999) #bufsize:9999
        try:
            print("resp latin-1 ", resp)
            respStr = resp.decode('latin-1')
        except UnicodeDecodeError:
            try:
                print("resp ascii ", resp)
                respStr = resp.decode('ascii')
            except UnicodeDecodeError:
                try:
                    print("resp utf-8 ", resp)
                    respStr = resp.decode('utf-8')
                except UnicodeDecodeError:
                    respStr = ''
                    return ''
        buff += respStr
        print("respStr ", respStr)
    # if searchReg:
    #     if searchReg.search(buff):
    #         return True, buff
    #     else:
    #         return False, buff
    #
    # else:
    #     return True, buff
def remote_run(hostname, User, Password, breakEvent):
    try:
        # 创建一个ssh客户端client对象
        ssh = paramiko.SSHClient()
        # 获取客户端host_keys,默认~/.ssh/known_hosts， 非默认路径需指定
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 创建ssh连接
        ssh.connect(hostname=hostname, username=User, password=Password)
        try:
            channel = ssh.invoke_shell()
            if User != 'root':
                #switch to root
                sendAndReceive(channel, "su -", "Password: ")
                sendAndReceive(channel, "r00t", "root-# ")
        except Exception as e:
            print('Error appear when do ssh operation: {0}'.format(e))
        finally:
            if channel:
                channel.close()

    except Exception as e:
        print('SSH connect server failed: {0}'.format(e))
    finally:
        if ssh:
            # 关闭ssh连接
            ssh.close()
        breakEvent.set()
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
        print("heartCount ", heartCount)
        if breakEvent.isSet():
            break
        time.sleep(1)
        heartCount += 1
    if not breakEvent.isSet():
        print('Operation timeout, {0} seconds passed.'.format(timeout))
if __name__ == '__main__':
    if len(sys.argv) != 1:
        usage()
    hostname = '135.242.106.251'
    User = 'ainet'
    Password = "ainet1"

    breakEvent = threading.Event()

    restart_thread = threading.Thread(target=remote_run, args = (hostname, User, Password, breakEvent))
    # restart_thread.start()
    # restart_thread.join()

    restart_thread.setDaemon(True)
    restart_thread.start()

    timeout = 30
    heart_thread = threading.Thread(target=heartBeat, args = (timeout, breakEvent,  ))
    heart_thread.start()
    heart_thread.join()

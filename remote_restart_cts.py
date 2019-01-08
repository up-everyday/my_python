# -*- coding:UTF-8 -*-
'''
基于用户名和密码实现 SSH远程登录，并在远程服务器上执行命令
'''
import paramiko

hostname = '135.242.106.251'
username = 'root'
password = "r00t"

# 创建一个ssh客户端client对象
ssh = paramiko.SSHClient()
# 获取客户端host_keys,默认~/.ssh/known_hosts， 非默认路径需指定
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 创建ssh连接
ssh.connect(hostname=hostname, username=username, password=password)
# 调用远程执行命令方法exec_command()
stdin,stdout,stderr=ssh.exec_command('/u/ainet/cts/bin/restart_cts')
# 打印命令执行结果，得到Python列表形式，可以使用stdout.readlines()
result = stdout.readlines()
print(result)
stdin,stdout,stderr=ssh.exec_command('ps -ef | grep pser')
# 打印命令执行结果，得到Python列表形式，可以使用stdout.readlines()
result = stdout.readlines()
print(result)
# 关闭ssh连接
ssh.close()

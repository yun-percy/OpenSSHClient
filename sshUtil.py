#!/usr/bin/python
#-*- coding:utf-8 -*-
#此脚本用来登录常用的服务器
import commands
import sys
import os
import pexpect
import termios
import struct
import fcntl
import signal
import time
from pexpect import pxssh
import getpass
#-------------参数区---------------------
home=os.environ['HOME']
config_file=os.path.join(home,'.serve')
number=1
addr=[]
port=[]
name=[]
passwd=[]
selected=False
new_serve=False
file_exist=False
ssh=None
old_time=time.time()
#-------------函数区---------------------
def print_usetime():
    global old_time
    now_time=time.time()
    print int(now_time)-int(old_time)
    old_time=now_time
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    LIGHT_BLUE = '\033[36m'
    WARNING_ORANGE = '\033[33m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
def sigwinch_passthrough (sig, data):
    winsize = getwinsize()
    global ssh
    ssh.setwinsize(winsize[0],winsize[1])
def getwinsize():
    """This returns the window size of the child tty.
    The return value is a tuple of (rows, cols).
    """
    if 'TIOCGWINSZ' in dir(termios):
        TIOCGWINSZ = termios.TIOCGWINSZ
    else:
        TIOCGWINSZ = 1074295912L # Assume
    s = struct.pack('HHHH', 0, 0, 0, 0)
    x = fcntl.ioctl(sys.stdout.fileno(), TIOCGWINSZ, s)
    return struct.unpack('HHHH', x)[0:2]
def login_serve():
    if server_port == '':
        cmd='ssh '+server_addr
    else:
        cmd='ssh -p '+server_port+' '+server_addr
    ret=os.system(cmd)
    return ret
def ssh_cmd(port,addr, passwd,cmd):
    global ssh
    ret = -1
    ssh = pexpect.spawn("""ssh -p %s %s '%s'""" % (port,addr,cmd))
    signal.signal(signal.SIGWINCH, sigwinch_passthrough)
    winsize = getwinsize()
    ssh.setwinsize(winsize[0], winsize[1])
    print """ssh -p %s %s '%s'""" % (port,addr,cmd)
    try:
        i = ssh.expect(['password:', 'continue connecting (yes/no)?','Password:'], timeout=5)
        if i == 0 :
            ssh.sendline(passwd)
        elif i == 1:
            ssh.sendline('yes\n')
            ssh.expect('password: ')
            ssh.sendline(passwd)
        if i == 2 :
            ssh.sendline(passwd)
        return ssh
    except pexpect.EOF:
        print "EOF"
        ssh.close()
        ret = -1
    except pexpect.TIMEOUT:
        print "TIMEOUT"
        ssh.close()
        ret = -2
    return ret
def pxssh_cmd(addr,port,passwd,cmd):
    try:
        # 调用构造函数，创建一个 pxssh 类的对象:
        s = pxssh.pxssh()
        # 获得用户指定 ssh 主机域名.
        hostname = addr.split['@'][-1]
        # 获得用户指定 ssh 主机用户名.
        username = addr.split['@'][0]
        # 获得用户指定 ssh 主机密码.
        # password = getpass.getpass('password: ')
        # 利用 pxssh 类的 login 方法进行 ssh 登录，原始 prompt 为'$' , '#'或'>'
        s.login (hostname, username, passwd, original_prompt='[$#>]')
        # 发送命令 'uptime'
        s.sendline ('uptime')
        # 匹配 prompt
        s.prompt()
        # 将 prompt 前所有内容打印出，即命令 'uptime' 的执行结果.
        print s.before
        # 发送命令 ' ls -l '
        s.sendline (cmd )
        # 匹配 prompt
        s.prompt()
        # 将 prompt 前所有内容打印出，即命令 ' ls -l ' 的执行结果.
        ret=s.before
        # 退出 ssh session
        s.logout()
        return ret
    except pxssh.ExceptionPxssh, e:
        print "pxssh failed on login."
        print str(e)

def outputResult(port, addr, passwd,cmd):
    print_usetime()
    child=ssh_cmd(port, addr, passwd,cmd)
    print child
    print_usetime()
    if type(child)==type(0):
        return "ERROR"
    else:
        child.expect(pexpect.EOF)
        return child.before
#-------------流程区---------------------
def main():
    port=22
    addr="percy@192.168.1.1"
    passwd="passwd"
    cmd='ls file'
    outputResult(port, addr, passwd, cmd)
if __name__ == '__main__':
    main()

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
#-------------函数区---------------------
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
def outputResult(port, addr, passwd,cmd):
    child=ssh_cmd(port, addr, passwd,cmd)
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

#!/usr/bin/env python
# coding=utf-8

from pexpect import pxssh
import getpass
def pxssh_cmd(addr,port,passwd,cmd):
    try:
        # 调用构造函数，创建一个 pxssh 类的对象:
        s = pxssh.pxssh()
        # 获得用户指定 ssh 主机域名.
        # print addr.split()
        hostname = addr.split('@')[-1]
        # 获得用户指定 ssh 主机用户名.
        username = addr.split('@')[0]
        # 获得用户指定 ssh 主机密码.
        # password = getpass.getpass('password: ')
        # 利用 pxssh 类的 login 方法进行 ssh 登录，原始 prompt 为'$' , '#'或'>'
        s.login (hostname, username, passwd, original_prompt='[$#>]')
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
        return str(e)

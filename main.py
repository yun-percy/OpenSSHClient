#!/usr/bin/env python
# coding=utf-8
# import wxversion
# wxversion.select('3.0')
import wx
import os
import sys
import time
import sshUtil
import shutil
import commands
import getpass

# import wx.lib.buttons as buttons

app=wx.App()
title='远程SSH管理器'
addr_hint_str='远程地址：'
addr_hint_str='端口：'
passwd_hint_str='密码: '
default_addr='%s@localhost' % getpass.getuser()
default_port='22'
default_passwd='passwd'
# file_path_abs='~'
space=10
win_size_x=wx.DisplaySize()[0]/2
win_size_y=wx.DisplaySize()[1]/2
menu_height=25
file_list_weight=150
file_list_height=win_size_y-menu_height-space*5
d = [u'test'] * 30
class OpenSSHClient(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,title=title,
            pos=(win_size_x/2,win_size_y/2),size=(win_size_x,win_size_y),
            style=wx.DEFAULT_FRAME_STYLE,name='frame')
        panel=wx.Panel(self,-1,)
        if 'phoenix' in wx.PlatformInfo:
            hand_cursor = wx.Cursor(wx.CURSOR_HAND)
        else:
            hand_cursor = wx.StockCursor(wx.CURSOR_HAND)
        self.addr_hint_text=wx.StaticText(panel,-1,label=addr_hint_str)
        self.addr_text=wx.TextCtrl(panel,-1,default_addr,size=(200,-1))
        self.port_hint_text=wx.StaticText(panel,-1,label=addr_hint_str)
        self.port_text=wx.TextCtrl(panel,-1,default_port,size=(30,-1))
        self.passwd_hint_text=wx.StaticText(panel,-1,label=passwd_hint_str)
        self.passwd_text=wx.TextCtrl(panel,-1,default_passwd,size=(80,-1))
        #主体元素
        self.filelistbox = wx.ListBox(panel, 60,(-1,-1),(file_list_weight,file_list_height), d, wx.LB_SINGLE)
        self.Bind(wx.EVT_LISTBOX, self.EvtListBox, self.filelistbox)
        self.filedetail = wx.StaticText(panel,-1,size=(file_list_weight*4,file_list_height))
        #开始布局.
        # mainSizer is the top-level one that manages everything mainSizer是最水平的布局器
        #2 垂直的sizer
        mainSizer = wx.BoxSizer(wx.VERTICAL)#垂直布局
        # addrSizer is a grid that holds all of the address info
        #添加第一行地址栏
        header_sizer=wx.FlexGridSizer(rows=1,hgap=15,vgap=15)
        header_sizer.Add(self.addr_hint_text,0,wx.EXPAND)
        header_sizer.Add(self.addr_text, 0,wx.EXPAND)
        header_sizer.Add(self.port_hint_text,0,wx.EXPAND)
        header_sizer.Add(self.port_text, 0,wx.EXPAND)
        header_sizer.Add(self.passwd_hint_text,0,wx.EXPAND)
        header_sizer.Add(self.passwd_text, 0,wx.EXPAND)
        header_sizer.AddGrowableCol(1)
        mainSizer.Add(header_sizer, 0, wx.EXPAND|wx.ALL, 10)
        mainSizer.Add(wx.StaticLine(panel), 0,wx.EXPAND|wx.TOP|wx.BOTTOM, 5)#添加一条水平线
        #添加文件列表，文件详情
        context_sizer=wx.FlexGridSizer(rows=1,hgap=15,vgap=15)
        context_sizer.AddGrowableCol(1,4)
        context_sizer.AddGrowableCol(0,1)
        context_sizer.AddGrowableRow(0)
        context_sizer.Add(self.filelistbox,flag=wx.EXPAND,proportion=wx.EXPAND)
        context_sizer.Add(self.filedetail,flag=wx.EXPAND,proportion=wx.EXPAND)
        mainSizer.Add(context_sizer, wx.EXPAND, wx.EXPAND|wx.ALL, 10)
        mainSizer.Add(wx.StaticLine(panel), 0,wx.EXPAND|wx.TOP|wx.BOTTOM, 5)#添加一条水平线
        # # 添加动作按钮栏
        # action_sizer=wx.FlexGridSizer(rows=1,hgap=15,vgap=15)
        # action_sizer.Add(self.refresh_btn,wx.ALIGN_CENTER,wx.ALIGN_CENTER)
        # action_sizer.Add(self.new_pos_btn,wx.ALIGN_CENTER,wx.ALIGN_CENTER)
        # action_sizer.Add(self.edit_pos_btn,wx.ALIGN_CENTER,wx.ALIGN_CENTER)
        # # action_sizer.Add(self.release_btn,wx.ALIGN_CENTER,wx.ALIGN_CENTER)
        # action_sizer.Add(self.exit_btn,wx.ALIGN_CENTER,wx.ALIGN_CENTER)
        # mainSizer.Add(action_sizer, 0, wx.ALL|wx.ALIGN_RIGHT, 10)
        # mainSizer.AddGrowableCol(1)
        panel.SetSizer(mainSizer)
        mainSizer.Fit(self)
        mainSizer.SetSizeHints(self)


        # self.new_pos_btn=wx.Button(panel,-1,'新建')
        # self.new_pos_btn.SetDefault()
        # self.edit_pos_btn=wx.Button(panel,-1,'编辑')
        #
        # # self.release_btn.Bind(wx.EVT_BUTTON, self.ReleaseToGithub)
        # self.exit_btn=wx.Button(panel,-1,'退出')
        # self.refresh_btn=wx.Button(panel,-1,'刷新文章')
        # # self.new_pos_btn.Bind(wx.EVT_BUTTON, self.NewFile)
        # # self.exit_btn.Bind(wx.EVT_BUTTON,self.ExitBlogManager)
        # # self.refresh_btn.Bind(wx.EVT_BUTTON,self.reloadPostList)
        # # self.edit_pos_btn.Bind(wx.EVT_BUTTON,self.EditPost)
        #
        #
        # # self.lb1.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        #
        # # for wxMSW
        # # self.lb1.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick)
        #
        # # for wxGTK
        # # self.lb1.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
        #
        # # self.getPostList(default_location)
        # # default_post_location=self.lb1.GetClientData(self.lb1.GetSelection())
        # # self.generate_markdown_preview(default_post_location)
        # # 添加动作按钮栏
        # action_sizer=wx.FlexGridSizer(rows=1,hgap=15,vgap=15)
        # action_sizer.Add(self.refresh_btn,wx.ALIGN_CENTER,wx.ALIGN_CENTER)
        # action_sizer.Add(self.new_pos_btn,wx.ALIGN_CENTER,wx.ALIGN_CENTER)
        # action_sizer.Add(self.edit_pos_btn,wx.ALIGN_CENTER,wx.ALIGN_CENTER)
        # # action_sizer.Add(self.release_btn,wx.ALIGN_CENTER,wx.ALIGN_CENTER)
        # action_sizer.Add(self.exit_btn,wx.ALIGN_CENTER,wx.ALIGN_CENTER)
        # mainSizer.Add(action_sizer, 0, wx.ALL|wx.ALIGN_RIGHT, 10)
        # # mainSizer.AddGrowableCol(1)
        # panel.SetSizer(mainSizer)
        # mainSizer.Fit(self)
        # mainSizer.SetSizeHints(self)
        # self.Bind(wx.EVT_CLOSE, self.closewindow)
        # self.Bind(wx.wx.EVT_QUERY_END_SESSION, wx.CloseEvent)
        print time.time()
        self.InitSSHFileList()
    def EvtListBox(self, event):
        lb = event.GetEventObject()
        # print lb.GetSelection()
        data = lb.GetClientData(lb.GetSelection())
        if data['type']=='dir':
            # cmd='ls -al %s' % data['path']
            self.flash_file_list(data['path'])

    def InitSSHFileList(self):
        # cmd='ls -al'
        self.flash_file_list('~')
    def flash_file_list(self,path):
        # global file_path_abs
        addr=self.addr_text.GetLineText(0)
        port=self.port_text.GetLineText(0)
        passwd=self.passwd_text.GetLineText(0)
        cmd='ls -al %s' % path
        ret=sshUtil.outputResult(port, addr, passwd, cmd)
        filelist=ret.strip().split(os.linesep)
        print ret
        del filelist[0]#删掉总结的字符串 例如"total 160"
        del filelist[0]#删掉第一排的字符串 例如"."
        self.filelistbox.Clear()
        # self.filelistbox.Append("..")
        for i in range(0,len(filelist)):
            file_name=filelist[i].split(':')[-1].split()[-1]
            permission=filelist[i].split()[0]
            if list(permission)[0]=='d':
                file_type="dir"
                file_name='%s%s' %(file_name,os.sep)
                file_path_abs=os.path.join(path,file_name)
            elif list(permission)[0]=='l':
                file_type="link"
            else :
                file_type='file'
                file_path_abs=os.path.join(path,file_name)
            filedetail={}
            filedetail['path']=file_path_abs
            filedetail['type']=file_type
            # post_name=fileUtil.getPostNamebyPath(article_path_abs)
            # print post_name,article_path_abs
            print i,filelist[i]
            self.filelistbox.Append(file_name)
            self.filelistbox.SetClientData(i, filedetail);
        self.filelistbox.SetSelection(0)
frame =OpenSSHClient()
frame.Show()
app.MainLoop()

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import wx
import sys
from time import sleep
from threading import Thread
from select import *
from socket import *


class MyFrame(wx.Frame):

    def __init__(self,
                 parent=None,
                 id=-1,
                 title='chatroom',
                 pos=(400, 100),
                 size=(500, 500)
                 ):
        super(MyFrame, self).__init__(parent, id, title, pos, size)
        self.SetFrame()

    def SetFrame(self):
        # create a panel first
        panel = wx.Panel(self)
        self.setBox(panel)

    def setBox(self, panel):
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)

        self.r1 = wx.StaticText(panel, -1, "聊天记录")

        self.r2 = wx.TextCtrl(panel,
                              value="love you ",
                              size=(600, 300),
                              style=wx.TE_READONLY | wx.TE_LEFT | wx.TE_MULTILINE)

        self.r3 = wx.StaticText(panel, -1, "输入框")
        self.my_message = wx.TextCtrl(panel,
                                      wx.ID_ANY,
                                      wx.EmptyString,
                                      wx.DefaultPosition,
                                      wx.Size(600, 100),
                                      wx.TE_MULTILINE)
        self.my_message.SetFont(wx.Font(15, 70, 90, 90, False, wx.EmptyString))

        self.my_button = wx.Button(panel,
                                   wx.ID_ANY,
                                   u"发送",
                                   wx.DefaultPosition,
                                   wx.Size(80, -1), 0)
        self.my_button.SetFont(wx.Font(15, 70, 90, 90, False, wx.EmptyString))

        hbox1.Add(self.r1, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        hbox2.Add(self.r2, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        hbox3.Add(self.r3, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        hbox4.Add(self.my_message, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        hbox5.Add(self.my_button, 1, wx.EXPAND | wx.ALIGN_RIGHT | wx.ALL, 5)

        vbox.Add(hbox1)
        vbox.Add(hbox2)
        vbox.Add(hbox3)
        vbox.Add(hbox4)
        vbox.Add(hbox5)

        self.r1.Bind(wx.EVT_TEXT, None)
        self.r3.Bind(wx.EVT_TEXT, None)
        self.my_message.Bind(wx.EVT_TEXT_ENTER, self.OnEnterPressed)
        self.my_button.Bind(wx.EVT_BUTTON, self.OnEnterPressed)

        panel.SetSizer(vbox)

        self.Centre()
        self.Show()

        self.Fit()

    def OnEnterPressed(self, event):
        print("in enter")
        l = wx.TextCtrl.GetNumberOfLines(self.r2)
        print(l, "l")
        msg1 = str(self.my_message.GetLineText(0))
        msg2 = str(self.my_message.GetLineText(1))
        msg = "我：\n" + msg1 + msg2
        print(msg)
        self.r2.AppendText("\n" + msg)
        self.my_message.Clear()
        self.my_message.SetInsertionPoint(0)
        print("out from enter")

    def OnMaxLen(self, event):
        print("Maximum length reached")


class App(wx.App):

    def OnInit(self):
        self.frame = MyFrame(size=(600, 600))

        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True


class Client(MyFrame):

    def __init__(self, ADDR):
        MyFrame.__init__(self, size=(600, 600))

        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.ADDR = ADDR
        print(self.ADDR)

    def MainServer(self):
        print("child thread")
        rlist = [self.s]
        wlist = []
        elist = [self.s]
        BUFFER = 4096

        self.s.connect((self.ADDR))

        while True:
            print("IO conplexing")
            rl, wl, el = select(rlist, wlist, elist)
            for i in rl:
                if i == self.s:
                    print("in for of rl")
                    msg = self.s.recv(BUFFER).decode()
                    self.r2.AppendText("\n" + msg)
                    print(msg)


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 8063
    ADDR = (HOST, PORT)
    app = App()
    C = Client(ADDR)
    T = Thread(target=C.MainServer)
    T.start()
    # print("before")
    # p = Process(target=C.MainServer)
    # p.start()
    app.MainLoop()

    T.join()
    # p.join()

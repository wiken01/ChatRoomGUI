# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from select import *
from socket import *
from threading import Thread
from chatFrame import *


class Client():

    def __init__(self):
        self.HOST = "127.0.0.1"
        self.PORT = 8064
        self.ADDR = (self.HOST, self.PORT)

        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def receive(self):
        self.s.connect(self.ADDR)
        print("connected")
        print("in receive")
        rlist = [self.s]
        wlist = []
        elist = []
        BUFFER = 4096
        while True:
            print("IO conplexing")
            rl, wl, el = select(rlist, wlist, elist)
            for i in rl:
                if i == self.s:
                    print("in for of rl")
                    msg = self.s.recv(BUFFER).decode()
                    # MyFrame.r2.AppendText("\n" + msg)
                    print(msg)


if __name__ == "__main__":
    c = Client()
    c.receive()

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from socket import *


class Murder(object):

    def __init__(self, ADDR):
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.s.bind(ADDR)
        self.s.listen(10)
        self.addr = ADDR

    def begin(self):
        print("waiting for connect")
        c, addr = self.s.accept()
        print("connected")
        while True:
            print(" while in server")
            msg = input("input:")
            c.send(msg.encode())
            print("sended")


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 8064
    ADDR = (HOST, PORT)
    m = Murder(ADDR)
    m.begin()

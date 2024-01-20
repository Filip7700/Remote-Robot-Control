# -*- coding: utf-8 -*-

import socket as sc



class ClientRobotControl:
    def __init__(self, hostname, port, buffersize):
        self.hostname = hostname
        self.port = port
        self.buffersize = buffersize
        self.clientsocket = ''
        self.hostip = ''



    def setupconnection(self):
        print('Trying to connect to robot...')
        self.clientsocket = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
        self.hostip = sc.gethostbyname(self.hostname)
        self.clientsocket.connect((self.hostip, self.port))

        print('hostname: {0}, ip: {1}'.format(self.hostname, self.hostip))



    def closeconnection(self):
        self.clientsocket.close()



    def sendstring(self, s):
        stringsize = len(s)
        stringtosend = s[0 : stringsize - 1]

        if stringsize > self.buffersize:
            stringtosend = s[0 : self.buffersize - 1]

        self.clientsocket.send(stringtosend.encode())



    def receivestring(self):
        receivedbytes = self.clientsocket.recv(self.buffersize)
        s = receivedbytes.decode()
        return s



    def sendint(self, intgr):
        bytestosend = intgr.to_bytes(intgr, 'little')
        self.clientsocket.send(bytestosend)



    def receiveint(self):
        receivedbytes = self.clientsocket.recv(self.buffersize)
        intgr = int.from_bytes(receivedbytes, 'little')

        return intgr

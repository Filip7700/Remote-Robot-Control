# -*- coding: utf-8 -*-

import socket as sc



class ServerRobotControl:
    def __init__(self, targetport, connectionscount, buffersize):
        self.targetport = targetport
        self.connectionscount = connectionscount
        self.buffersize = buffersize

        self.selfsocket = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
        self.selfsocket.bind(('', self.targetport))
        self.selfsocket.listen(self.connectionscount)

        self.targetsocket = ''
        self.targetaddress = ''



    def waitforconnection(self):
        print('Waiting for connection...')
        self.targetsocket, self.targetaddress = self.selfsocket.accept()
        print('Connection established! IP: {0}'.format(self.targetaddress))



    def closeconnection(self):
        self.targetsocket.close()



    def sendstring(self, s):
        stringsize = len(s)
        stringtosend = s[0 : stringsize - 1]

        if stringsize >= self.buffersize:
            stringtosend = s[0 : self.buffersize - 1]

        self.targetsocket.send(stringtosend.encode())



    def receivestring(self):
        receivedbytes = self.targetsocket.recv(self.buffersize)
        s = receivedbytes.decode()
        return s



    def sendint(self, intgr):
        bytestosend = intgr.to_bytes(intgr, 'little')
        self.targetsocket.send(bytestosend)



    def receiveint(self):
        receivedbytes = self.targetsocket.recv(self.buffersize)
        receivedbytescount = len(receivedbytes)

        if receivedbytescount == 0:
            raise OSError('Error: Client has been abruptly disconnected.')

        intgr = int.from_bytes(receivedbytes, 'little')

        return intgr

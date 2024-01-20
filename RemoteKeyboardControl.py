# -*- coding: utf-8 -*-

import pynput.keyboard as kb
import ClientRobotControl as cl
import RobotCommandDictionary as rcd



class RemoteKeyboardControl:
    def __init__(self, robotclient):
        self.robotclient = robotclient
        self.iskeypressed = False
        self.robotcommands = rcd.RobotCommandDictionary()



    def onkeypress(self, k):
        ret = True

        try:
            kchr = k.char

            if self.iskeypressed == False:
                print('Key pressed: {0}'.format(kchr))
                self.iskeypressed = True

                cmd = self.robotcommands.getcommandfromstring(kchr)

                if cmd == rcd.RobotCommandDictionaryEnum.ROBOTSHUTDOWN:
                    self.robotclient.sendint(cmd.value)
                    self.robotclient.closeconnection()
                    ret = False
                else:
                    self.robotclient.sendint(cmd.value)
        except AttributeError as e:
            print(e)

        return ret



    def onkeyrelease(self, k):
        ret = True

        try:
            kchr = k.char

            if self.iskeypressed == True:
                print('Key released: {0}'.format(kchr))
                self.iskeypressed = False

                cmd = self.robotcommands.getcommandfromstring(kchr)
                iscommandtogglable = (
                    self.robotcommands.getcommandtogglability(cmd))

                if cmd == rcd.RobotCommandDictionaryEnum.ROBOTSHUTDOWN:
                    ret = False
                elif iscommandtogglable == False:
                    self.robotclient.sendint(cmd.value)

        except AttributeError as e:
            print(e)

        return ret



    def runremotekeyboardcontrol(self):
        self.robotclient.setupconnection()

        with kb.Listener(on_press = self.onkeypress,
            on_release = self.onkeyrelease) as keylistener:

            keylistener.join()

# -*- coding: utf-8 -*-

from enum import Enum



class RobotCommandDictionaryEnum(Enum):
    MOTORPWMENABLE         =  1
    MOTORPWMDISABLE        =  2
    MOTORIDLE              =  3
    MOTORSPEEDUP           =  4
    MOTORSLOWDOWN          =  5
    MOTORDIRECTIONFORWARD  =  6
    MOTORDIRECTIONLEFT     =  7
    MOTORDIRECTIONBACKWARD =  8
    MOTORDIRECTIONRIGHT    =  9
    ROBOTSHUTDOWN          = 10
    INVALIDCOMMAND         = 11



class RobotCommandDictionary:
    def __init__(self):
        self.commanddictionary = {
            'n': RobotCommandDictionaryEnum.MOTORPWMENABLE,
            'm': RobotCommandDictionaryEnum.MOTORPWMDISABLE,
            'c': RobotCommandDictionaryEnum.MOTORIDLE,
            '+': RobotCommandDictionaryEnum.MOTORSPEEDUP,
            '-': RobotCommandDictionaryEnum.MOTORSLOWDOWN,
            'w': RobotCommandDictionaryEnum.MOTORDIRECTIONFORWARD,
            'a': RobotCommandDictionaryEnum.MOTORDIRECTIONLEFT,
            's': RobotCommandDictionaryEnum.MOTORDIRECTIONBACKWARD,
            'd': RobotCommandDictionaryEnum.MOTORDIRECTIONRIGHT,
            'q': RobotCommandDictionaryEnum.ROBOTSHUTDOWN
        }

        self.inversecommanddictionary = {
            RobotCommandDictionaryEnum.MOTORPWMENABLE:         'n',
            RobotCommandDictionaryEnum.MOTORPWMDISABLE:        'm',
            RobotCommandDictionaryEnum.MOTORIDLE:              'c',
            RobotCommandDictionaryEnum.MOTORSPEEDUP:           '+',
            RobotCommandDictionaryEnum.MOTORSLOWDOWN:          '-',
            RobotCommandDictionaryEnum.MOTORDIRECTIONFORWARD:  'w',
            RobotCommandDictionaryEnum.MOTORDIRECTIONLEFT:     'a',
            RobotCommandDictionaryEnum.MOTORDIRECTIONBACKWARD: 's',
            RobotCommandDictionaryEnum.MOTORDIRECTIONRIGHT:    'd',
            RobotCommandDictionaryEnum.ROBOTSHUTDOWN:          'q'
        }

        self.togglabilitycommanddictionary = {
            RobotCommandDictionaryEnum.MOTORPWMENABLE:         True,
            RobotCommandDictionaryEnum.MOTORPWMDISABLE:        True,
            RobotCommandDictionaryEnum.MOTORIDLE:              True,
            RobotCommandDictionaryEnum.MOTORSPEEDUP:           True,
            RobotCommandDictionaryEnum.MOTORSLOWDOWN:          True,
            RobotCommandDictionaryEnum.MOTORDIRECTIONFORWARD:  False,
            RobotCommandDictionaryEnum.MOTORDIRECTIONLEFT:     False,
            RobotCommandDictionaryEnum.MOTORDIRECTIONBACKWARD: False,
            RobotCommandDictionaryEnum.MOTORDIRECTIONRIGHT:    False,
            RobotCommandDictionaryEnum.ROBOTSHUTDOWN:          True
        }



    def getcommandfromstring(self, s):
        cmd = RobotCommandDictionaryEnum.INVALIDCOMMAND

        try:
            cmd = self.commanddictionary[s]
        except KeyError:
            print('Key {0} not found in the robot command dictionary.'
                .format(s))

        return cmd



    def getcommandfromvalue(self, val):
        cmd = RobotCommandDictionaryEnum.INVALIDCOMMAND

        for robotcommand in (RobotCommandDictionaryEnum):
            if val == robotcommand.value:
                cmd = robotcommand

        return cmd



    def getstringfromcommand(self, cmd):
        s = ''

        try:
            s = self.inversecommanddictionary[cmd]
        except:
            print('Key {0} not found in the inverse robot command dictionary.'
                .format(cmd))

        return s



    def getcommandtogglability(self, cmd):
        togglability = False

        if cmd != RobotCommandDictionaryEnum.INVALIDCOMMAND:
            togglability = self.togglabilitycommanddictionary[cmd]

        return togglability



    def getcommandtogglabilityfromstring(self, s):
        cmd = self.getcommandfromstring(s)
        togglability = self.getcommandtogglability(cmd)

        return togglability


    def getcommandtogglabilityfromvalue(self, val):
        cmd = self.getcommandfromvalue(val)
        togglability = self.getcommandtogglability(cmd)

        return togglability

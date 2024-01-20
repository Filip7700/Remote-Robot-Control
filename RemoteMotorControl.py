# -*- coding: utf-8 -*-

import time
import RPi.GPIO as gpio
import ServerRobotControl as sr
import RobotCommandDictionary as rcd



class RemoteMotorControl:
    def __init__(self, robotserver, pwmfrequencyinhz,
        ena, in1, in2, in3, in4, enb):

        self.defaultdutycycle = 50.0
        self.maxdutycycle = 100.0
        self.mindutycycle = 25.0
        self.dutycyclechange = 10.0
        self.sleeptimeinseconds = 0.001

        self.motordutycycle = self.defaultdutycycle

        self.robotcommands = rcd.RobotCommandDictionary()

        self.robotserver = robotserver
        self.ena = ena
        self.in1 = in1
        self.in2 = in2
        self.in3 = in3
        self.in4 = in4
        self.enb = enb

        self.pwma = ''
        self.pwmb = ''
        self.setupgpios(pwmfrequencyinhz)

        self.robotcommandstates = {
            rcd.RobotCommandDictionaryEnum.MOTORPWMENABLE:         False,
            rcd.RobotCommandDictionaryEnum.MOTORPWMDISABLE:        False,
            rcd.RobotCommandDictionaryEnum.MOTORIDLE:              False,
            rcd.RobotCommandDictionaryEnum.MOTORSPEEDUP:           False,
            rcd.RobotCommandDictionaryEnum.MOTORSLOWDOWN:          False,
            rcd.RobotCommandDictionaryEnum.MOTORDIRECTIONFORWARD:  False,
            rcd.RobotCommandDictionaryEnum.MOTORDIRECTIONLEFT:     False,
            rcd.RobotCommandDictionaryEnum.MOTORDIRECTIONBACKWARD: False,
            rcd.RobotCommandDictionaryEnum.MOTORDIRECTIONRIGHT:    False,
            rcd.RobotCommandDictionaryEnum.ROBOTSHUTDOWN:          False
        }



    def setupgpios(self, pwmfrequencyinhz):
        gpio.setmode(gpio.BCM)
        gpio.setup(self.ena, gpio.OUT)
        gpio.setup(self.in1, gpio.OUT)
        gpio.setup(self.in2, gpio.OUT)
        gpio.setup(self.in3, gpio.OUT)
        gpio.setup(self.in4, gpio.OUT)
        gpio.setup(self.enb, gpio.OUT)

        gpio.output(self.in1, gpio.LOW)
        gpio.output(self.in2, gpio.LOW)
        gpio.output(self.in3, gpio.LOW)
        gpio.output(self.in4, gpio.LOW)

        self.pwma = gpio.PWM(self.ena, pwmfrequencyinhz)
        self.pwmb = gpio.PWM(self.enb, pwmfrequencyinhz)



    def enablemotors(self):
        self.pwma.start(self.motordutycycle)
        self.pwmb.start(self.motordutycycle)

        print('Motors enabled.')



    def disablemotors(self):
        gpio.output(self.in1, gpio.LOW)
        gpio.output(self.in2, gpio.LOW)
        gpio.output(self.in3, gpio.LOW)
        gpio.output(self.in4, gpio.LOW)
        self.pwma.stop()
        self.pwmb.stop()

        print('Motors disabled!')



    def resetcommandstates(self):
        for cmd in self.robotcommandstates:
            self.robotcommandstates[cmd] = False



    def idlemotors(self):
        gpio.output(self.in1, gpio.LOW)
        gpio.output(self.in2, gpio.LOW)
        gpio.output(self.in3, gpio.LOW)
        gpio.output(self.in4, gpio.LOW)

        self.resetcommandstates()

        print('Motors are stacionary.')



    def applynewmotorsdirection(self):
        f = self.robotcommandstates[
            rcd.RobotCommandDictionaryEnum.MOTORDIRECTIONFORWARD]

        l = self.robotcommandstates[
            rcd.RobotCommandDictionaryEnum.MOTORDIRECTIONLEFT]

        b = self.robotcommandstates[
            rcd.RobotCommandDictionaryEnum.MOTORDIRECTIONBACKWARD]

        r = self.robotcommandstates[
            rcd.RobotCommandDictionaryEnum.MOTORDIRECTIONRIGHT]

        # Forward
        if f == True:
            gpio.output(self.in2, gpio.LOW)
            gpio.output(self.in4, gpio.LOW)
            gpio.output(self.in1, gpio.HIGH)
            gpio.output(self.in3, gpio.HIGH)

            self.pwma.ChangeDutyCycle(self.motordutycycle)
            self.pwmb.ChangeDutyCycle(self.motordutycycle)

        # Left
        elif l == True:
            gpio.output(self.in1, gpio.LOW)
            gpio.output(self.in4, gpio.LOW)
            gpio.output(self.in2, gpio.HIGH)
            gpio.output(self.in3, gpio.HIGH)

            self.pwma.ChangeDutyCycle(self.motordutycycle)
            self.pwmb.ChangeDutyCycle(self.motordutycycle)

        # Backward
        elif b == True:
            gpio.output(self.in1, gpio.LOW)
            gpio.output(self.in3, gpio.LOW)
            gpio.output(self.in2, gpio.HIGH)
            gpio.output(self.in4, gpio.HIGH)

            self.pwma.ChangeDutyCycle(self.motordutycycle)
            self.pwmb.ChangeDutyCycle(self.motordutycycle)

        # Right
        elif r == True:
            gpio.output(self.in2, gpio.LOW)
            gpio.output(self.in3, gpio.LOW)
            gpio.output(self.in1, gpio.HIGH)
            gpio.output(self.in4, gpio.HIGH)

            self.pwma.ChangeDutyCycle(self.motordutycycle)
            self.pwmb.ChangeDutyCycle(self.motordutycycle)

        # All other invalid cases stop motors
        else:
            gpio.output(self.in1, gpio.LOW)
            gpio.output(self.in2, gpio.LOW)
            gpio.output(self.in3, gpio.LOW)
            gpio.output(self.in4, gpio.LOW)

            self.pwma.ChangeDutyCycle(self.motordutycycle)
            self.pwmb.ChangeDutyCycle(self.motordutycycle)



    def updatemotorsdirection(self, cmd):
        cmdstate = self.robotcommandstates[cmd]
        newcmdstate = cmdstate ^ True
        self.robotcommandstates[cmd] = newcmdstate

        self.applynewmotorsdirection()

        print('Motors direction updated.')



    def increasemotorsdutycycle(self):
        newmotordutycycle = (
            self.motordutycycle
            + self.dutycyclechange)

        if newmotordutycycle > self.maxdutycycle:
            self.motorpdutycycle = self.maxdutycycle
        elif newmotordutycycle < self.mindutycycle:
            self.motordutycycle = self.mindutycycle
        else:
            self.motordutycycle = newmotordutycycle

        self.pwma.ChangeDutyCycle(self.motordutycycle)
        self.pwmb.ChangeDutyCycle(self.motordutycycle)

        print('New motor duty cycle: {0}.'.format(self.motordutycycle))



    def decreasemotorsdutycycle(self):
        newmotordutycycle = (
            self.motordutycycle
            - self.dutycyclechange)

        if newmotordutycycle > self.maxdutycycle:
            self.motorpdutycycle = self.maxdutycycle
        elif newmotordutycycle < self.mindutycycle:
            self.motordutycycle = self.mindutycycle
        else:
            self.motordutycycle = newmotordutycycle

        self.pwma.ChangeDutyCycle(self.motordutycycle)
        self.pwmb.ChangeDutyCycle(self.motordutycycle)

        print('New motor duty cycle: {0}.'.format(self.motordutycycle))



    def cleargpios(self):
        gpio.output(self.in1, gpio.LOW)
        gpio.output(self.in2, gpio.LOW)
        gpio.output(self.in3, gpio.LOW)
        gpio.output(self.in4, gpio.LOW)
        self.pwma.stop()
        self.pwmb.stop()

        gpio.cleanup()

        print('GPIOs clered!')



    def executecommand(self, command):
        isgoingtoshutdown = False

        if command == rcd.RobotCommandDictionaryEnum.MOTORPWMENABLE:
            self.enablemotors()
        elif command == rcd.RobotCommandDictionaryEnum.MOTORPWMDISABLE:
            self.disablemotors()
        elif command == rcd.RobotCommandDictionaryEnum.MOTORIDLE:
            self.idlemotors()
        elif command == rcd.RobotCommandDictionaryEnum.MOTORSPEEDUP:
            self.increasemotorsdutycycle()
        elif command == rcd.RobotCommandDictionaryEnum.MOTORSLOWDOWN:
            self.decreasemotorsdutycycle()
        elif command == rcd.RobotCommandDictionaryEnum.MOTORDIRECTIONFORWARD:
            self.updatemotorsdirection(command)
        elif command == rcd.RobotCommandDictionaryEnum.MOTORDIRECTIONLEFT:
            self.updatemotorsdirection(command)
        elif command == rcd.RobotCommandDictionaryEnum.MOTORDIRECTIONBACKWARD:
            self.updatemotorsdirection(command)
        elif command == rcd.RobotCommandDictionaryEnum.MOTORDIRECTIONRIGHT:
            self.updatemotorsdirection(command)
        elif command == rcd.RobotCommandDictionaryEnum.ROBOTSHUTDOWN:
            self.cleargpios()
            isgoingtoshutdown = True
        else:
            print('Invalid command: {0}! Ignoring...'.format(command))

        return isgoingtoshutdown



    def runremotemotorcontrol(self):
        isrunning = True

        self.robotserver.waitforconnection()

        while isrunning == True:
            try:
                cmdval = self.robotserver.receiveint()
                cmd = self.robotcommands.getcommandfromvalue(cmdval)

                ret = self.executecommand(cmd)

                if ret == True:
                    isrunning = False

                time.sleep(self.sleeptimeinseconds)
            except OSError as e:
                print(e)
                self.cleargpios()
                isrunning = False

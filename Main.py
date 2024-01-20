# -*- coding: utf-8 -*-

isserver = False

try:
    import ServerRobotControl as sr
    import RemoteMotorControl as rmc

    isserver = True

except ModuleNotFoundError:
    import ClientRobotControl as cl
    import RemoteKeyboardControl as rkc



port = 4600
connectionscount = 1
buffersize = 16
pwmfreqinhz = 120.0
rpihostname = 'raspberrypi'



def initializeremotemotors():
    global port
    global connectionscount
    global buffersize
    global pwmfreqinhz

    srctrl = sr.ServerRobotControl(port, connectionscount, buffersize)

    motorctrl = rmc.RemoteMotorControl(srctrl, pwmfreqinhz,
        12, 17, 27, 22, 23, 13)

    return motorctrl



def initializeremotekeyboard():
    global port
    global buffersize
    global rpihostname

    clctrl = cl.ClientRobotControl(rpihostname, port, buffersize)
    kbctrl = rkc.RemoteKeyboardControl(clctrl)

    return kbctrl



def main():
    global isserver

    if isserver == True:
        remotemotorcontroller = initializeremotemotors()
        remotemotorcontroller.runremotemotorcontrol()
    else:
        remotekeyboardcontroller = initializeremotekeyboard()
        remotekeyboardcontroller.runremotekeyboardcontrol()

    print('Goodbye!')



if __name__ == '__main__':
    main()

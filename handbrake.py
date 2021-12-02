import sys
import glob
import serial
import keyboard
from tkinter import *


def serial_ports():
    """Takes a list of the available serial ports

    Returns
    -------
    list
        A list constaining the available serial ports

    Raises
    ------
    EnvironmentError
        If there is an error
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def main(args):
    """main func

    Parameters
    ----------
    args tuple: 
        command line args
    """

    print("Program started!")

    ports = serial_ports()

    p = ""
    for port in ports:
        p += port + "\n"

    #select the serial port
    loop = True
    while loop:
        port = input("Choose a serial port:\n%s\n\n>>>" % (p))
        if port not in ports:
            print("Invalid choice!")
            continue
        loop = False


    #create comunication channel
    arduino = serial.Serial(port=port, baudrate=9600, timeout=.1)

   controll = False
	#read the arduino serial inputs
    while True:
        s = arduino.readline().strip()
        if (s==b'X'):
            controll = True
        elif (s==b'Y'):
            controll = False
        
		#press "p" key on the keyboard
        if controll:
            keyboard.press('p')
        else:
            keyboard.release('p')



if __name__ == '__main__':
    main(sys.argv)

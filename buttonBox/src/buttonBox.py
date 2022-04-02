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


    arduino = serial.Serial(port, baudrate=9600, timeout=0.1)

    print("Button Box operational!\nSelected port: %s\nDetecting arduino inputs.\nClose the window to leave." % (port))


    #read inputs from the arduino and press the corresponding keyboard keys
    while True:
        try:
            s = arduino.readline().strip()
        except:
            print("ERRO: Unable to access port %s!" % (port))
            break
        if (s==b'0'):
            keyboard.press_and_release("0")
        elif (s==b'2'):
            keyboard.press_and_release("2")
        elif (s==b'3'):
            keyboard.press_and_release("3")
        elif (s==b'4'):
            keyboard.press_and_release("4")
        elif (s==b'5'):
            keyboard.press_and_release("5")
        elif (s==b'6'):
            keyboard.press_and_release("6")
        elif (s==b'7'):
            keyboard.press_and_release("7")
        elif (s==b'8'):
            keyboard.press_and_release("8")
        elif (s==b'9'):
            keyboard.press_and_release("9")
        elif (s==b'L'):
            keyboard.press_and_release("p")
        elif (s==b'1'):
            keyboard.press_and_release("1")
        elif (s==b'R'):
            keyboard.press_and_release("o")


if __name__ == '__main__':
    print("Program started.")

    main(sys.argv)

    print("Program terminated!")

import sys
import glob
import serial
import keyboard
import json
import time


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


def portsCom():
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

    #create the config file with the selected port
    try:
        with open("settings.json", "w") as f:
            f.write(json.dumps({"port":port}, indent=4))

    except:
        print("ERROR: Impossible to create configuration file!")
        return port

    print("Created a configuration file: settings.json")

    return port


def main(args):
    """main func
    Parameters
    ----------
    args tuple: 
        command line args
    """

    try:
        with open("settings.json", "r") as f:
            config = json.loads(f.read())
        port = config["port"]
    except:
        print("No configuration detected.")
        port = portsCom()


    arduino = serial.Serial(port, baudrate=9600, timeout=0.1)

    print("Button Box operational!\nDetecting button box inputs on port %s.\nClose the window to exit." % (port))

    delay = 0.01

    #read inputs from the arduino and press the corresponding keyboard keys
    while True:
        try:
            s = arduino.readline().strip()
        except:
            print("ERRO: Unable to access port %s!" % (port))
            return

        if (s==b'0'):
            keyboard.press("0")
            time.sleep(delay)
            keyboard.release("0")
        elif (s==b'1'):
            keyboard.press("1")
            time.sleep(delay)
            keyboard.release("1")
        elif (s==b'2'):
            keyboard.press("2")
            time.sleep(delay)
            keyboard.release("2")
        elif (s==b'3'):
            keyboard.press("3")
            time.sleep(delay)
            keyboard.release("3")
        elif (s==b'4'):
            keyboard.press("4")
            time.sleep(delay)
            keyboard.release("4")
        elif (s==b'5'):
            keyboard.press("5")
            time.sleep(delay)
            keyboard.release("5")
        elif (s==b'6'):
            keyboard.press("6")
            time.sleep(delay)
            keyboard.release("6")
        elif (s==b'7'):
            keyboard.press("7")
            time.sleep(delay)
            keyboard.release("7")
        elif (s==b'8'):
            keyboard.press("8")
            time.sleep(delay)
            keyboard.release("8")
        elif (s==b'9'):
            keyboard.press("9")
            time.sleep(delay)
            keyboard.release("9")
        elif (s==b'L'):
            keyboard.press("i")
            time.sleep(delay)
            keyboard.release("i")
        elif (s==b'R'):
            keyboard.press("o")
            time.sleep(delay)
            keyboard.release("o")


if __name__ == '__main__':
    print("Program started.")

    main(sys.argv)

    print("Program terminated!")

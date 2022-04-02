from glob import glob
import sys
import glob
import serial
import keyboard

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


def connect_arduino(port: str):
    """Connect to the arduino on the given serial port

    Args:
        port (str): the port to connect
    """
    #create comunication channel
    arduino = serial.Serial(port=port, baudrate=9600, timeout=.01)

    print("Successfully created communication channel on port " + port)

    return arduino


def data_exchange_arduino(arduino, rpm: str):
    """Writes the rpm values and then reads the state of the handbrake\n
    If the handbrake is pressed, the keyboard coorrespondent is pressed

    Args:
        arduino (Serial): the serial communication channel where the arduino is connected to
        rpm (str): the revolutions per minute gotten from the selected game
    """

    # write the rpm values to light up the rev lights
    arduino.write(bytes(rpm, 'utf-8'))

    # read the handbrake state and press the button
    s = arduino.read()

    # handbrake is pulled
    if (s==b'X'):
        keyboard.press('p')

    # handbrake is released
    elif (s==b'Y'):
        keyboard.release('p')
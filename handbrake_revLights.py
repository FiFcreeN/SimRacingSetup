import sys
import glob
import serial
import keyboard
import json

from fdp import *
import socket


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

    print("Program started!")

    #configure ports and sockets
    UDP_PORT = 5607

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', UDP_PORT))

    params = ForzaDataPacket.get_props(packet_format="fh4")

    try:
        with open("settings.json", "r") as f:
            config = json.loads(f.read())
        port = config["port"]
    except:
        print("No configuration detected.")
        port = portsCom()



    #create comunication channel
    arduino = serial.Serial(port=port, baudrate=9600, timeout=.01)

    print("Successfully created communication channel on port " + port)

    #send rpm data to arduino
    control = False
    while True:

        try:
            message, address = server_socket.recvfrom(1024)
            fdp = ForzaDataPacket(message, packet_format = "fh4")
            
            rpm_values = fdp.to_list(params)[2:5]
            rpm = "%d/%d\n" % (rpm_values[2], rpm_values[0])
        
        except:
            rpm = ""

        arduino.write(bytes(rpm, 'utf-8'))

        s = arduino.read()

        if (s==b'X'):
            control = True
        elif (s==b'Y'):
            control = False

        if control:
            keyboard.press('p')
        else:
            keyboard.release('p')

if __name__ == '__main__':
    main(sys.argv)
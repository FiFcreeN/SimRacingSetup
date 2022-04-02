from json import loads, dumps
from SerialComs import serial_ports

def portsCom() -> str:
    """Select a serial port to communicate with an arduino

    Returns:
        str: the serial port selected
    """

    ports = serial_ports()

    p = ""
    for i in range(len(ports)):
        p += "%d - " % (i+1) + ports[i] + "\n"


    #select the serial port
    i = 0
    while i - 1 not in range(len(ports)):
        i = int(input("Choose a serial port:\n%s\n\n>>>" % (p)))

        # error message
        if i - 1 not in range(len(ports)):
            print("Invalid option!")
        
    create_configs(ports[i-1])

    return ports[i-1]

def load_configs():
    """Tries to read a config file to look for a serial port.\n
    If it doesn't exist, a new one is created

    Returns:
        str: the serial port
    """
    # try to read the configs file
    try:
        with open("settings.json", "r") as f:
            config = loads(f.read())
        port = config["port"]

    # create a new file if it doesn't exist
    except:
        print("No configuration detected.")
        port = portsCom()

    return port


def create_configs(port: str):
    """Creates a settings file with the selected port

    Args:
        port (str): the selected port
    """

    #create the config file with the selected port
    try:
        with open("settings.json", "w") as f:
            f.write(dumps({"port":port}, indent=4))

    except:
        print("ERROR: Impossible to create configuration file!")
        return port

    print("Created a configuration file: settings.json")
from SerialComs import connect_arduino, data_exchange_arduino
from ConfigFiles import load_configs

def forzaUDP():
    """communicate with arduino after recieving FH UDP data
    """
    # Forza Horizon module
    from fdp import ForzaDataPacket
    import socket

    #configure ports and sockets
    UDP_PORT = 5607

    # create the udp sockets
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', UDP_PORT))

    # setup the Forza module to forza horizon 4 compatibility
    params = ForzaDataPacket.get_props(packet_format="fh4")

    # connect to the arduino
    arduino = connect_arduino(load_configs())


    #send rpm data to arduino
    while True:

        # Rev lights
        try:
            message, address = server_socket.recvfrom(1024)
            fdp = ForzaDataPacket(message, packet_format = "fh4")
            
            rpm_values = fdp.to_list(params)[2:5]
            rpm = "%d/%d\n" % (rpm_values[2], rpm_values[0])
        
        except:
            rpm = ""

        data_exchange_arduino(arduino, rpm)



def pc2UDP():
    """comunicate with arduino after recieving pc2 UDP data
    """
    # module for interpreting project cars udp data
    from pcars.stream import PCarsStreamReceiver

    # instance the stream reciever
    stream = PCarsStreamReceiver()

    #create comunication channel
    arduino = connect_arduino(load_configs())

    #send rpm data to arduino
    while True:
        try:
            rpm_values = stream.getValues()
            rpm = "%d/%d\n" % (rpm_values[0]*0.95, rpm_values[1])
        except:
            rpm = ""

        data_exchange_arduino(arduino, rpm)
from SerialComs import connect_arduino, data_exchange_arduino
from ConfigFiles import load_configs

def forzaUDP():
    """communicate with arduino after recieving FH UDP data
    """
    # Forza Horizon module
    from fdp import ForzaDataPacket
    import socket


    # create the udp sockets
    UDP_PORT = 5607
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


def f1_2021_UDP():
    from f1_2021 import telemetry, header
    import socket

    # stream
    obj_header = header.Header()
    obj_telemetry = telemetry.PacketCarTelemetryData()

    # create the udp sockets
    UDP_PORT = 5607
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', UDP_PORT))

    # connect to arduino
    arduino = connect_arduino(load_configs())


    while True:
        # recieve data
        data = server_socket.recv(2048)

        # unpack data
        if data:
            obj_header.unpack_struct(obj_header.packet_format, data)

            if obj_header.m_packetId == 6:
                packet_format = obj_header.packet_format + obj_telemetry.packet_format
                obj_telemetry.unpack_struct(packet_format, data)

            # convert the engine rpm
            rev_lights_percent = obj_telemetry.m_carTelemetryData[obj_header.m_playerCarIndex].m_revLightsPercent.value

            data_exchange_arduino(arduino, "%d/100\n" % (rev_lights_percent))




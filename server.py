#imports
import socket
import struct
import tkinter as tk

#list of clients
connected_clients_sockets = []
#socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Tkinter window and object to save canvas
rootWindow = tk.Tk()
Currcanvas = tk.Canvas(rootWindow)


#Create a packet to send
def createPacket(format, type, payload):
    structInfo = struct.Struct(format)
    canvasStr = payload.toDataURL()
    packedInfo = struct.pack(format, type, canvasStr.encode("UTF-8"))
    return packedInfo

#main
while True:
    #variables
    port = 60
    ip = '192.168.1.107'

    #bind server to ip and port to listen on
    serverAddrObj = (ip, port)
    sock.bind(serverAddrObj)

    #wait for client
    sock.listen(1)
    print("Waiting for connection...")

    #Connect to client
    connection_obj, client_addr = sock.accept()
    print("Connected client: " + str(client_addr))

    format = 'is'
    unpacker = struct.Struct(format)

    try:
        while True:
            #recieve data from client
            packed_data = connection_obj.recv(unpacker.size())
            data = unpacker.unpack(packed_data)
            Currcanvas = data[1].decode()

            type = 1
            packetToSend = createPacket(format, type, Currcanvas)
            sock.sendall(packetToSend)
    except KeyboardInterrupt:
        sock.close()
    except:
        sock.close()
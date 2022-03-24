#GROUP 7
#Kee Boon Hwee, 2101797
#Foo Seow Wei, Edward, 2101258
#Lim Jin Thong, 2100913
#Tong Hui Qing, Glennice, 2101569
#Teo Leng, 2102311

import socket
import threading
import queue
import os
class ChatServer:
    #-----------------------------------------------------------------------------------------------
    def __init__(self, userName, portNumber=7):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.ip = s.getsockname()[0]
        self.port = int(portNumber)                                            # RFC 862 echo protocol states TCP port = 7
        s.close()
        self.socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self.server_address = ( self.ip, self.port )
        self.socket.bind(self.server_address)
        print('Chat Server on ipv4 {}, is listening on port {}...'.format(*self.server_address))
        self.CMD_LIST     = "LIST images"
        self.CMD_DOWNLOAD = "DOWNLOAD"
        self.imageList = ["a.png", "b.png"]
        self.quitFlag = False
        self.userName = userName
        self.clientCount = 0
        self.clientThread = {}
        self.connections = {}
        self.messageQueue = queue.Queue()
        self.echoThread   = threading.Thread(target = self.Echo)
        self.echoThread.start()
        self.inputThread = threading.Thread(target = self.Input)
        self.inputThread.start()
        self.listenThread = threading.Thread(target = self.Listen)
        self.listenThread.start()
        self.echoThread.join()
        self.inputThread.join()
        self.listenThread.join()
    #-----------------------------------------------------------------------------------------------
    def Listen(self):
        self.socket.listen(512)
        while(not self.quitFlag):
            try:
                connection, client_address = self.socket.accept()
                self.clientCount += 1
                newClient = str(client_address[1]) + str(self.clientCount)
                print("New connection received from " + str(newClient) + " (" + str(self.clientCount) + " connection(s)!")
                client = threading.Thread(target = self.AcceptConnection , args=( connection , client_address ) ).start()
                self.connections[ client_address ] = connection
                self.clientThread[ client_address ] = client
            except Exception as e:
                print("Server listen() error : " + str(e))
    #-----------------------------------------------------------------------------------------------
    def Echo(self):
        while(not self.quitFlag):
            if self.messageQueue.qsize() > 0:
                message = self.messageQueue.get()
                if(message[0] == self.userName):
                    msg = message[0] + " > " + message[1]
                    msg = bytearray( msg , 'UTF-8')
                    for id, cn in self.connections.items():
                        if cn != None:
                            cn.sendall( msg )
                else:
                    uN,ms = str(message[1]).split(" > ")
                    if ms == self.CMD_LIST:
                        for id, cn in self.connections.items():
                            if str(id[1]) == str(message[0]):
                                try:
                                    cn.sendall(bytearray(str(self.imageList), 'UTF-8'))
                                except Exception as c:
                                    print(str(c))
                    if self.CMD_DOWNLOAD in ms:
                        fileName = ms.split(" ")[1]
                        print(fileName)
                        for id, cn in self.connections.items():
                            if str(id[1]) == str(message[0]):
                                if fileName in self.imageList:
                                    file = open(fileName, 'rb')
                                    imgSize = os.path.getsize(fileName)
                                    sendClientSize = "Size:" + str(imgSize)
                                    cn.sendall(bytearray(str(sendClientSize),'UTF-8'))
                                    d = 0
                                    while d <= imgSize:
                                        data = file.read(1024)
                                        if not data:
                                            print("Send completed")
                                            break
                                        cn.sendall(data)
                                        d += len(data)
                                else:
                                    cn.sendall(bytearray(str("ERROR"),'UTF-8'))
                    else:
                        print("\n" + message[1] )
                        for id, cn in self.connections.items():
                            if str(id[1]) != str(message[0]):
                                try:
                                    cn.sendall( bytearray( message[1] , 'UTF-8') )
                                except Exception as c:
                                    print(str(c))
                    

    #-----------------------------------------------------------------------------------------------
    def Input(self):
        while(not self.quitFlag):
            yourmessage = input("")
            self.messageQueue.put( (self.userName , yourmessage) )
    #-----------------------------------------------------------------------------------------------
    def AcceptConnection(self,connection,client_address):
        try:
            while(True):
                data = connection.recv(512)           # This must be the same as the client, and vice versa
                if data:
                    self.messageQueue.put( (str(client_address[1]), bytes(data).decode('UTF-8') ) )
        except Exception as e:
            connection.close()
            self.connections[ client_address ] = None
            self.connections.pop(client_address)
            self.clientCount -= 1
            print("\n" + str(e))
    #-----------------------------------------------------------------------------------------------
    def __del__(self):
        for id, client in self.clientThread.items():
            client.join()
        self.socket.close()
        print("\nCharServer has terminated.\n")
    #-----------------------------------------------------------------------------------------------

def main():
    try:
        print("This is CSC1010 chat server : ")
        portNotSet = True
        while portNotSet:
            try:
                port = int(input("Please specify the listening port number : "))
                portNotSet = False
            except:
                pass
        name = input("Please enter your chat moniker : ")
        server = ChatServer(name,port)

    except Exception as e:
        if server is not None:
            server.close()
            server = None
        print(str(e))

if __name__ == "__main__":
    main()
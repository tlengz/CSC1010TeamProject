import socket
import threading
import queue

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
        self.CMD_DOWNLOAD = "DOWNLOAD image.jpg"
        self.quitFlag = False
        self.userName = userName
        self.clientCount = 0
        self.clients = {}
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
        self.socket.listen(128)
        while(not self.quitFlag):
            connection, client_address = self.socket.accept()
            self.clientCount += 1
            newClient = str(client_address[1]) + str(self.clientCount)
            print("New connection received from " + str(newClient) + " (" + str(self.clientCount) + " connection(s)!")
            self.clients[ newClient ] = connection

            client = threading.Thread(target = self.AcceptConnection , args=[ connection , client_address[1] ] )
            client.start()
            client.join()
    #-----------------------------------------------------------------------------------------------
    def Echo(self):
        while(not self.quitFlag):
            if self.messageQueue.qsize() > 0:
                message = self.messageQueue.get()
                if(message[0] == self.userName):
                    msg = message[0] + " > " + message[1]
                    msg = bytearray( msg , 'UTF-8')
                    for id, cn in self.clients.items():
                        cn.sendall( msg )
                else:
                    print("\n" + message[1] )
    #-----------------------------------------------------------------------------------------------
    def Input(self):
        while(not self.quitFlag):
            yourmessage = input("")
            self.messageQueue.put( (self.userName , yourmessage) )
    #-----------------------------------------------------------------------------------------------
    def AcceptConnection(self,connection,address):
        try:
            while(True):
                data = connection.recv(64)           # This must be the same as the client, and vice versa
                if data:
                    self.messageQueue.put( (str(address), bytes(data).decode('UTF-8') ) )
        except Exception as e:
            connection.close()
            self.clients.pop(connection)
            print("\n" + str(e))
    #-----------------------------------------------------------------------------------------------
    def __del__(self):
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
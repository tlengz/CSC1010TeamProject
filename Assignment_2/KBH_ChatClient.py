import socket
import threading
import queue

class ChatClient:
    #-----------------------------------------------------------------------------------------------
    def __init__(self, userName, portNumber=7):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = int(portNumber)                                            # RFC 862 echo protocol states TCP port = 7
        self.socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self.server_address = ( "192.168.0.124", self.port )
        self.socket.connect(self.server_address)
        print('Chat Client on ipv4 {}, is listening on port {}...'.format(*self.server_address))
        self.CMD_LIST     = "LIST images"
        self.CMD_DOWNLOAD = "DOWNLOAD image.jpg"
        self.quitFlag = False
        self.userName = userName
        self.messageQueue = queue.Queue()
        self.echoThread   = threading.Thread(target = self.Echo)
        self.echoThread.start()
        self.inputThread = threading.Thread(target = self.Input)
        self.inputThread.start()
        self.listenThread = threading.Thread(target = self.Receiver)
        self.listenThread.start()
        self.echoThread.join()
        self.inputThread.join()
        self.listenThread.join()
    #-----------------------------------------------------------------------------------------------
    def Echo(self):
        while(not self.quitFlag):
            if self.messageQueue.qsize() > 0:
                message = self.messageQueue.get()
                if(message[0] == self.userName):
                    msg = message[0] + " > " + message[1]
                    msg = bytearray( msg , 'UTF-8')
                    self.socket.sendall( msg )
                else:
                    print("\n" + message[1] )
    #-----------------------------------------------------------------------------------------------
    def Input(self):
        while(not self.quitFlag):
            yourmessage = input("")
            self.messageQueue.put( (self.userName , yourmessage) )
    #-----------------------------------------------------------------------------------------------
    def Receiver(self):
        try:
            while(not self.quitFlag):
                data = self.socket.recv(64)           # This must be the same as the client, and vice versa
                if data:
                    self.messageQueue.put( (str("Server"), bytes(data).decode('UTF-8') ) )
        except Exception as e:
            print("\n" + str(e))
    #-----------------------------------------------------------------------------------------------
    def __del__(self):
        self.socket.close()
        print("\nCharClient has terminated.\n")
    #-----------------------------------------------------------------------------------------------

def main():
    try:
        print("This is CSC1010 chat client : ")
        portNotSet = True
        while portNotSet:
            try:
                port = int(input("Please specify the listening port number : "))
                portNotSet = False
            except:
                pass
        name = input("Please enter your chat moniker : ")
        client = ChatClient(name,port)

    except Exception as e:
        if client is not None:
            client.close()
            client = None
        print(str(e))

if __name__ == "__main__":
    main()
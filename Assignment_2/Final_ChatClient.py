#GROUP 7
#Kee Boon Hwee, 2101797
#Foo Seow Wei, Edward, 2101258
#Lim Jin Thong, 2100913
#Tong Hui Qing, Glennice, 2101569
#Teo Leng, 2102311

import socket
import threading
import queue

class ChatClient:
    # -----------------------------------------------------------------------------------------------
    def __init__(self, userName, portNumber=7):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = int(portNumber)  # RFC 862 echo protocol states TCP port = 7
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ("172.30.140.103", self.port)
        self.socket.connect(self.server_address)
        print('Chat Client on ipv4 {}, is listening on port {}...'.format(*self.server_address))
        self.CMD_LIST = "LIST images"
        self.CMD_DOWNLOAD = "DOWNLOAD"
        self.imageInLIst = False
        self.imageSize = 0
        self.DownloadImg = False
        self.fileName = ""
        self.quitFlag = False
        self.userName = userName
        self.messageQueue = queue.Queue()
        self.echoThread = threading.Thread(target=self.Echo)
        self.echoThread.start()
        self.inputThread = threading.Thread(target=self.Input)
        self.inputThread.start()
        self.listenThread = threading.Thread(target=self.Receiver)
        self.listenThread.start()
        self.echoThread.join()
        self.inputThread.join()
        self.listenThread.join()


    # -----------------------------------------------------------------------------------------------
    def Echo(self):
        while not self.quitFlag:
            if self.messageQueue.qsize() > 0:
                message = self.messageQueue.get()
                if (message[0] == self.userName):
                    msg = message[0] + " > " + message[1]
                    msg = bytearray(msg, 'UTF-8')
                    self.socket.sendall(msg)
                else:
                    if not self.DownloadImg:
                        print("\n" + message[1])
                    else:
                        if "ERROR" in str(message[1]):
                            self.imageSize = 0
                            print("image does not exist")
                            self.DownloadImg = False

                        if "Size:" in str(message[1]):
                            self.imageSize = str(message[1]).split(':')[1]
                            self.imageSize = int(self.imageSize)

    # -----------------------------------------------------------------------------------------------
    def Input(self):
        while not self.quitFlag:
            yourmessage = input("")
            if self.CMD_DOWNLOAD in yourmessage :
                self.DownloadImg = True
                self.fileName = yourmessage.split(" ")[1]
                self.fileName = "(1)" +self.fileName
            self.messageQueue.put((self.userName, yourmessage))

    # -----------------------------------------------------------------------------------------------
    def Receiver(self):
        try:
            while not self.quitFlag:
                if self.DownloadImg:
                    if self.imageSize > 0:
                        print("Downloading")
                        file = open(self.fileName,'wb')
                        c = 0
                        # Running the loop while file is recieved.
                        while c <= self.imageSize:
                            print(c)
                            if c >= self.imageSize:
                                break
                            data = self.socket.recv(1024)
                            file.write(data)
                            c += len(data)
                        file.close()
                        self.imageSize = 0
                        print("Download completed")
                        self.DownloadImg = False
                # This must be the same as the client, and vice versa
                elif not self.DownloadImg:
                    data = self.socket.recv(1024)
                    self.messageQueue.put((str("Server"), bytes(data).decode('UTF-8')))
        except Exception as e:
            print("\n" + str(e))

    # -----------------------------------------------------------------------------------------------
    def __del__(self):
        self.socket.close()
        print("\nCharClient has terminated.\n")
    # -----------------------------------------------------------------------------------------------


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
        print(name)
        client = ChatClient(name, port)


    except Exception as e:
        if client is not None:
            client.close()
            client = None
        print(str(e))


if __name__ == "__main__":
    main()

import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = 1612
        self.addr = (self.server,self.port)
        self.data = self.connect()
        self.pos = self.divdata()
        self.p = [1,2]
        
    def getPos(self):
        return self.pos
    
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except :
            pass
        
    def send(self,data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    def getP(self):
        if self.pos == "0,0":
            return self.p[0]
        else :
            return self.p[1]

    def divdata(self):
        if self.data != "True" or self.data != "False":
            return self.data
        else:
            pass

    def reset(self,data):
        try:
            self.client.send(str.encode(str(data)))
        except socket.error as e:
            print(e)


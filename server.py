
import socket
import threading

server = "192.168.0.104"
port = 1612
idcount = 0
pos = [(0,200),(0,300)]
readystat = [False,False]
finish = 0


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
    str(e)
    
s.listen()
print("Waiting for a connection, Server Started")


def read_pos(str):
    str = str.split(",")
    return int(str[0]),int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

def read_check(str):
    if str == "True":
        return True
    else:
        return False

def threaded_client(conn, player):
    global idcount
    conn.send(str.encode(make_pos(pos[player])))
    
    reply = ""
    while True:
        try:
            data = conn.recv(2048).decode()
            print(data)

            if data == "True" or data == "False":
                readystat[player] = read_check(data)

                if player == 1: #if it is player2
                    reply = readystat[0] #send player1's
                else:
                    reply = readystat[1]
                        
                print("Received: ",data)
                print("Sending: ",reply)
                conn.send(str.encode(str(reply)))
            elif data == "1":
                pos[1] = (0,200)
                pos[0] = (0,300)
                readystat[0] = False
                readystat[1] = False
            else:
                pos[player] = read_pos(data)
                
                if not data:
                    print("Disconnected")
                    break
                else:
                    if player == 1: #if it is player2
                        reply = pos[0] #send player1's
                    else:
                        reply = pos[1]
                        
                    print("Received: ",data)
                    print("Sending: ",reply)
                conn.send(str.encode(make_pos(reply)))   
        except :
            break
        
    print("Lost connection")
    try:
        print("Closing Game")
    except:
        pass
    idcount -= 1
    conn.close()


while idcount < 2:
    conn,addr = s.accept()
    print("Connected to", addr)

    t = threading.Thread(target=threaded_client, args=(conn, idcount))
    t.start()
    idcount += 1
    if idcount % 2 == 1:
        print("Wait for another connection....")


print("Can only connected by 2 clients")


    
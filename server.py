import socket
import threading
PORT = 6000
SERVER = socket.gethostbyname(socket.gethostname())

ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
clients, names = [], []
server = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)
server.bind(ADDRESS)
DISCONNECT_MESSAGE= "/DISCONNECT"
DISCONNECT_MESSAGE2= "/disconnect"
DISCONNECT_MESSAGE3= "/quit"
# function to start the connection
def startChat():
    print("server is working on " + SERVER)

    server.listen()

    while True:

        conn, addr = server.accept()
        conn.send("?NAME?".encode(FORMAT))
        name = conn.recv(1024).decode(FORMAT)
        names.append(name)
        clients.append(conn)

        print(f"Name is :{name}")

        broadcastMessage(f"{name} has joined.".encode(FORMAT))

        conn.send('Connection successful'.encode(FORMAT))

        thread = threading.Thread(target=handle,
                                  args=(conn, addr))
        thread.start()

        print(f"active connections {threading.activeCount() - 1}")


def handle(conn, addr):
    print(f"new connection {addr}")
    connected = True

    while connected:
        message = conn.recv(1024)
        if message.decode(FORMAT) == DISCONNECT_MESSAGE3:
            print("u are stpuid")
            connected=False
            break
        broadcastMessage(message)
        print(f"{addr}: "+ message.decode(FORMAT) )
    clients.remove(conn)
    conn.close()

def broadcastMessage(message):
    for client in clients:
        client.send(message)

startChat()
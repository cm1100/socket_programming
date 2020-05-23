import socket
import select

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR , 1)

server_socket.bind((IP, PORT))

server_socket.listen()

sockets_list = [server_socket]
clients = {}

def recieve_msg(client_socket):
     try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        message_length = int(message_header.decode("utf-8"))
        return {"header":message_header,"data":client_socket.recv(message_length)}

     except:
         return False


while True:                                         # read list, write list ,error list
    read_sockets, _,exception_sockets = select.select(sockets_list,[],sockets_list)



    for notified in read_sockets:

        if notified == server_socket:
            client_socket , client_address = server_socket.accept()

            user = recieve_msg(client_socket)
            if user is False:
                continue

            sockets_list.append(client_socket)
            print(client_socket)
            clients[client_socket] = user
            #print(client_address)

            print(f"accepted new connection from {client_address[0]}:{client_address[1]} as {user['data'].decode('utf-8')}")

        else:
            message = recieve_msg(notified)
            if message is False:
                print(f"closed connection from {clients[notified]['data'].decode('utf-8')}")
                sockets_list.remove(notified)
                del clients[notified]
                continue


            user = clients[notified]
            #print(type(user))
            print(f"recieved message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}  ")

                #client_socket
            for client in clients:
                if client !=notified:
                    client.send(user['header']+user['data']+message['header']+message['data'])
    for notified in exception_sockets:
        sockets_list.remove(notified)
        del clients[notified]









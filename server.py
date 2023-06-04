import socket
import select

Header_length=10
IP="127.0.0.1"
Port=1234

server_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

server_socket.bind((IP,Port))

server_socket.listen()

sockets_list=[server_socket]

clients = {}

def receive_message(client_socket):
    try:
        message_header=client_socket.recv(Header_length)
        if not len(message_header):
            return False
        message_length= int(message_header.decode('utf-8').strip())
        return {"header":message_header,"data":client_socket.recv(message_length)}

    except:
        return False
def Auto_re(a, b = None):
    action = a + "ing"
    bad_things = ["fighting", "bickering", "yelling", "complaining"] 
    good_things = ["singing", "hugging", "playing", "working"]
    alternatives = ["codeing", "singing", "sleeping","eating"]
    if action in bad_things:
        return "YES Time for {}".format(action)
    elif action in good_things:
        return "Not doing that.".format(action)
    elif action in alternatives:
        return "Yea,{} is an option".format(action)
    return "I don't understand!"
def Auto_re1(a, b = None):
    action= a+"ing"
    first_things = ["crying","walking","singing","playing"]
    if action in first_things:
        return "{} seems negative.".format(action)
    return "I don't care!"
def Auto_re2(a):
    return "yes I like it."
while True:
    read_sockets,_,exception_sockets=select.select(sockets_list,[],sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket :
            client_socket, client_Address= server_socket.accept()

            user=receive_message(client_socket)

            if user is False:
                continue
            sockets_list.append(client_socket)
            clients[client_socket]=user
            print(clients)
            print(f"Accepted new connection from {client_Address[0]}:{client_Address[1]} username:{user['data'].decode('utf-8')}")

        else:
            message = receive_message(notified_socket)
            if message is False:
                print(f"closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            else:
                user=clients[notified_socket]
                print(f"received message from {user['data'].decode('utf-8')}:{message['data'].decode('utf-8')}")
                
                for client_socket in clients:
                    if client_socket == notified_socket:
                        action = str(message['data'])
                        if "?" in action:
                            m="{}".format(Auto_re(action[22:-2]))
                        elif "!" in action:
                            m="{}".format(Auto_re1(action[12:15]))
                        elif "weather"in action or "house" in action or "flower" in action:
                            m="{}".format(Auto_re2(action))
                        else:
                            m="Error"
                        
                        message['data']=bytes(m,'utf-8')
                        client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
                        

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
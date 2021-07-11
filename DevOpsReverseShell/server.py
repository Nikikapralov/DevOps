import socket
import sys


# Create a socket, an entrance to our PC.
def create_socket():
    try:
        host = ''
        port = 20050
        sock = socket.socket()
    except socket.error:
        print('An error occurred!')
        return

    return host, port, sock


# Bind the socket and the host and start listening for anyone trying to connect.
def bind_socket_host(host, port, sock):
    try:
        sock.bind((host, port))
        sock.listen(5)
    except socket.error:
        print('Trying again...')
        bind_socket_host(host, port, sock)
    print('Success!')


# If we receive data from the listen function, we accept the connection.
# This data must be sent from the other server first!
# ip = address[0]
# port = address[1]

def accept_connection(sock):
    connection, address = sock.accept()
    send_commands(connection, sock)
    connection.close()


def send_commands(connection, sock):
    while True:
        cmd = input()
        if cmd == 'quit':
            connection.close()
            sock.close()
            sys.exit()
        encoded_command = str.encode(cmd)
        if len(encoded_command) > 0:
            connection.send(encoded_command)
            response = str(connection.recv(1024), 'utf-8')
            print(response)


def main():
    host, port, sock = create_socket()
    bind_socket_host(host, port, sock)
    accept_connection(sock)


main()

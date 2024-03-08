from socket import *
import socket
from threading import Thread
import ssl

# morse code dictionary
Dictionary = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.',
    'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--',
    'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...',
    'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
    ', ': '--..--', '.': '.-.-.-', '?': '..--..', '/': '-..-.', '-': '-....-',
    '(': '.-.-.', ')': '-.--.'
}

def handle_client(connectionSocket):
    while True:
        inp = connectionSocket.recv(2000).decode()
        if not inp:
            break
        else:
            print("Client is requesting:",inp)
            if all(char in {'.', '-', ' '} for char in inp):
                translated = decrypt(inp.upper())
            else:
                translated = encrypt(inp.upper())

            connectionSocket.send(translated.encode())

    connectionSocket.close()

def encrypt(msg):
    cipher = ''
    for letter in msg:
        if letter != ' ':
            cipher += Dictionary[letter] + ' '
        else:
            cipher += ' '
    return cipher

def decrypt(msg):
    msg += ' '
    decipher = ''
    citext = ''
    for letter in msg:
        if letter != ' ':
            i = 0
            citext += letter
        else:
            i += 1
            if i == 2:
                decipher += ' '
            else:
                decipher += list(Dictionary.keys())[list(Dictionary.values()).index(citext)]
                citext = ''
    return decipher

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen()
    print("Server is listening for connections...")

    while True:
        client_socket, _ = server_socket.accept()
        print("Client connected.")

        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile='server.crt', keyfile='private.key')
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 
        client_socket = context.wrap_socket(client_socket, server_side=True)

        handle_client(client_socket)
        client_socket.close()

if __name__ == "__main__":
    main()

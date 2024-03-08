from tkinter import *
from socket import *
import ssl

def send_receive_morse():
    morse_text = morse_entry.get()

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(('localhost', 12345))

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
    clientSocket = context.wrap_socket(clientSocket, server_hostname='muthu')

    clientSocket.send(morse_text.encode())

    translated = clientSocket.recv(2000)

    result_label.config(text='Translated from server: ' + translated.decode())

    clientSocket.close()

# Create the main window
window = Tk()
window.title("Morse Code Translator")
window.geometry("500x500")

morse_label = Label(window, text="Input text to be encoded/decoded:",font=('Arial', 14))
morse_entry = Entry(window,font=('Arial', 14))
translate_button = Button(window, text="Translate", command=send_receive_morse,font=('Arial', 14))
result_label = Label(window, text="Translated from server:",font=('Arial', 14))

morse_label.pack(pady=10)
morse_entry.pack(pady=10)
translate_button.pack(pady=10)
result_label.pack(pady=10)

window.mainloop()

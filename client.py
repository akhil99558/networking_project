import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Client configuration
HOST = '127.0.0.1'
PORT = 12345

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client")

        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
        self.chat_area.pack(padx=20, pady=5, expand=True, fill='both')
        self.chat_area.config(state=tk.DISABLED)

        self.message_entry = tk.Entry(root, width=50)
        self.message_entry.pack(padx=20, pady=5, fill='x')
        self.message_entry.bind("<Return>", self.send_message)

        self.connect_to_server()

    def connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((HOST, PORT))
        threading.Thread(target=self.receive_messages).start()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                self.chat_area.config(state=tk.NORMAL)
                self.chat_area.insert(tk.END, message + '\n')
                self.chat_area.config(state=tk.DISABLED)
                self.chat_area.yview(tk.END)
            except:
                break

    def send_message(self, event):
        message = self.message_entry.get()
        self.client_socket.send(message.encode('utf-8'))
        self.message_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()

import socket
import tkinter as tk
import threading

class TCPClientApp:
    def __init__(self, master):
        self.master = master
        master.title("TCP Socket Tester")

        self.host_label = tk.Label(master, text="Server IP:")
        self.host_label.pack()

        self.host_entry = tk.Entry(master)
        self.host_entry.pack()

        self.port_label = tk.Label(master, text="Server Port:")
        self.port_label.pack()

        self.port_entry = tk.Entry(master)
        self.port_entry.pack()

        self.connect_button = tk.Button(master, text="Connect", command=self.connect)
        self.connect_button.pack()

        self.status_label = tk.Label(master, text="")
        self.status_label.pack()

        self.messages = [
            ('Track 1', 'CC55CC5501000001020008008300040000000000'),  
            ('Track 2', 'CC55CC5501000001020008008300040001000000'),  
            ('Track 3', 'CC55CC5501000001020008008300040002000000'),  
            ('Track 4', 'CC55CC5501000001020008008300040003000000'),
            ('Track 5', 'CC55CC5501000001020008008300040004000000'),
            ('Pause  ', 'CC55CC5501000001020008008500040003000000'), 
        ]

        for message_name, hex_message in self.messages:
            button = tk.Button(master, text=message_name, command=lambda m=hex_message: self.send_message(m))
            button.pack()

        self.connection = None

    def connect(self):
        host = self.host_entry.get()
        port = int(self.port_entry.get())
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((host, port))
            self.status_label.config(text="Connected")
        except Exception as e:
            self.status_label.config(text="Error: " + str(e))

    def send_message(self, hex_message):
        if self.connection is None:
            self.status_label.config(text="Not connected")
            return
        try:
            message_bytes = bytes.fromhex(hex_message)
            self.connection.sendall(message_bytes)
            self.status_label.config(text="Message sent successfully.")
        except Exception as e:
            self.status_label.config(text="Error: " + str(e))

def start_client_gui():
    root = tk.Tk()
    app = TCPClientApp(root)
    root.mainloop()

def main():
    client_thread = threading.Thread(target=start_client_gui)
    client_thread.start()

if __name__ == "__main__":
    main()
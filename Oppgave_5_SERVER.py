# Import block
import cv2
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Server parameters
HOST = '0.0.0.0'
PORT = 9999

# Create UDP-socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

clients = []


# Define function for video controll
def video_stream():
    # Capture video from Webcam
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        if not ret:
            break

        # Showing video on server machine
        cv2.imshow('Server Webcam', frame)

        # Converting frames to JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        data = buffer.tobytes()

        # Sending frames to clients if exist
        for client in clients:
            try:
                # Break frames into packages for 65000 bytes each
                for i in range(0, len(data), 65000):
                    server_socket.sendto(data[i:i + 65000], client)
            except:
                clients.remove(client)

        if cv2.waitKey(1) == 27:  # Stops when press ESC
            break

    cam.release()
    cv2.destroyAllWindows()


# Define function for controll and handle of client-devices
def handle_clients():
    while True:
        msg, addr = server_socket.recvfrom(1024)
        if addr not in clients:
            clients.append(addr)
            print(f"New client connected: {addr}")
        if msg.decode('utf-16') == 'disconnect':
            clients.remove(addr)
            print(f"Client {addr} disconnected.")





# Define function for chats GUI
def start_gui():
    global chat_window
    chat_window = tk.Tk()
    chat_window.title("Chat")

    # Create chat feed
    chat_area = scrolledtext.ScrolledText(chat_window, wrap=tk.WORD, height=15, width=50)
    chat_area.pack(padx=10, pady=10)

    # Create input text field
    input_area = tk.Entry(chat_window, width=50)
    input_area.pack(padx=10, pady=5)
    

# Define function for sending text messages to chat (WORK IN PROGRESS)    
    def send_message(event=None):
        message = input_area.get()
        if message:
            chat_area.insert(tk.END, f"Server: {message}\n")
            chat_area.yview(tk.END)
            input_area.delete(0, tk.END)
            for client in clients:
                try:
                    server_socket.sendto(message.encode('utf-16'), client)
                except:
                    clients.remove(client)


# Some chat controll stuff
    input_area.bind("<Return>", send_message)

    chat_window.protocol("WM_DELETE_WINDOW", stop_program)
    chat_window.bind('<Escape>', stop_program)

    chat_window.mainloop()


# Define function to stop whole program
def stop_program(event=None):
    global running
    running = False
    chat_window.destroy()

# Launch video stream
threading.Thread(target=video_stream).start()

# launch client controll
threading.Thread(target=handle_clients).start()

# Launch chat GUI
start_gui()

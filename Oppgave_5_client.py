import cv2
import socket
import numpy as np
import threading
import tkinter as tk
from tkinter import scrolledtext

# Параметры клиента
SERVER_IP = 'SERVER_IP_ADDRESS'
PORT = 9999

# Создание UDP-сокета
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.sendto("connect".encode('utf-16'), (SERVER_IP, PORT))

def receive_video():
    data = b""
    
    while True:
        try:
            packet, _ = client_socket.recvfrom(65000)
            data += packet

            if len(packet) < 65000:
                frame = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
                if frame is not None:
                    cv2.imshow('Server stream', frame)
                data = b""

            if cv2.waitKey(1) == 27:
                break
        except:
            break

    client_socket.sendto("disconnect".encode('utf-16'), (SERVER_IP, PORT))
    client_socket.close()
    cv2.destroyAllWindows()

def start_chat_gui():
    global chat_window
    chat_window = tk.Tk()
    chat_window.title("Chat")

    # Создание поля для сообщений
    chat_area = scrolledtext.ScrolledText(chat_window, wrap=tk.WORD, height=15, width=50)
    chat_area.pack(padx=10, pady=10)

    # Поле для ввода сообщения
    input_area = tk.Entry(chat_window, width=50)
    input_area.pack(padx=10, pady=5)
    
    def send_message(event=None):
        message = input_area.get()
        if message:
            chat_area.insert(tk.END, f"You: {message}\n")
            chat_area.yview(tk.END)
            input_area.delete(0, tk.END)
            client_socket.sendto(message.encode('utf-16'), (SERVER_IP, PORT))
    
    input_area.bind("<Return>", send_message)

    chat_window.protocol("WM_DELETE_WINDOW", stop_program)
    chat_window.bind('<Escape>', stop_program)

    chat_window.mainloop()

def stop_program(event=None):
    global running
    running = False
    chat_window.destroy()

# Запуск видеопотока
threading.Thread(target=receive_video).start()

# Запуск графического интерфейса
start_chat_gui()

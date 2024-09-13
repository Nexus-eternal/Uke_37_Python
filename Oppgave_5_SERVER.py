import cv2
import socket
import struct
import threading
import tkinter as tk
from tkinter import scrolledtext

# Параметры сервера
HOST = '0.0.0.0'
PORT = 9999

# Создание UDP-сокета
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

clients = []

def video_stream():
    # Захват видео с веб-камеры
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        if not ret:
            break

        # Отображение видео на сервере
        cv2.imshow('Server Webcam', frame)

        # Кодирование кадра в JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        data = buffer.tobytes()

        # Если есть клиенты, отправляем им данные
        for client in clients:
            try:
                # Разбиение на пакеты по 65000 байт
                for i in range(0, len(data), 65000):
                    server_socket.sendto(data[i:i + 65000], client)
            except:
                clients.remove(client)

        if cv2.waitKey(1) == 27:  # Остановка при нажатии ESC
            break

    cam.release()
    cv2.destroyAllWindows()

def handle_clients():
    while True:
        msg, addr = server_socket.recvfrom(1024)
        if addr not in clients:
            clients.append(addr)
            print(f"New client connected: {addr}")
        if msg.decode('utf-16') == 'disconnect':
            clients.remove(addr)
            print(f"Client {addr} disconnected.")

def send_messages():
    while True:
        message = input("Server: ")
        for client in clients:
            try:
                client_socket.sendto(message.encode('utf-16'), client)
            except:
                clients.remove(client)

def start_gui():
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
            chat_area.insert(tk.END, f"Server: {message}\n")
            chat_area.yview(tk.END)
            input_area.delete(0, tk.END)
            for client in clients:
                try:
                    server_socket.sendto(message.encode('utf-16'), client)
                except:
                    clients.remove(client)
    
    input_area.bind("<Return>", send_message)

    chat_window.protocol("WM_DELETE_WINDOW", stop_program)
    chat_window.bind('<Escape>', stop_program)

    chat_window.mainloop()

def stop_program(event=None):
    global running
    running = False
    chat_window.destroy()

# Запуск видеопотока
threading.Thread(target=video_stream).start()

# Запуск обработки клиентов
threading.Thread(target=handle_clients).start()

# Запуск графического интерфейса
start_gui()

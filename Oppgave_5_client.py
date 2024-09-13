import cv2
import socket
import numpy as np
import threading

# Параметры клиента
SERVER_IP = 'SERVER_IP_ADDRESS'
PORT = 9999

# Создание UDP-сокета
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.sendto("connect".encode('utf-16'), (SERVER_IP, PORT))

# Функция для получения видеопотока
def receive_video():
    data = b""
    
    while True:
        try:
            # Получаем данные по UDP
            packet, _ = client_socket.recvfrom(65000)
            data += packet

            # Попробуем декодировать полученные данные как изображение
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

# Функция для отправки сообщений на сервер
def send_messages():
    while True:
        message = input("You: ")
        client_socket.sendto(message.encode('utf-16'), (SERVER_IP, PORT))

# Запуск потоков для видеопотока и чата
threading.Thread(target=receive_video).start()
threading.Thread(target=send_messages).start()

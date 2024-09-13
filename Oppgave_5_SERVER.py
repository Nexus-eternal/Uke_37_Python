import cv2
import socket
import struct
import threading

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
        # Получение сообщения от нового клиента
        msg, addr = server_socket.recvfrom(1024)
        if addr not in clients:
            clients.append(addr)
            print(f"New client connected: {addr}")
        if msg.decode('utf-16') == 'disconnect':
            clients.remove(addr)
            print(f"Client {addr} disconnected.")

# Запуск видеопотока
threading.Thread(target=video_stream).start()

# Запуск обработки клиентов
threading.Thread(target=handle_clients).start()

print("Server is running...")

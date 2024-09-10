import cv2
import socket
import pickle
import struct
 
# Настройки сокета
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind(('', 9999))  # Принимает все входящие подключения
 
print("Клиент запущен, ожидает данных от сервера...")
 
while True:
    # Получение длины данных
    packed_data, _ = client_socket.recvfrom(4096)
    data_len = struct.unpack("L", packed_data)[0]
    # Получение данных изображения
    frame_data, _ = client_socket.recvfrom(data_len)
    frame = pickle.loads(frame_data)  # Десериализация изображения
 
    # Отображение кадра
    cv2.imshow("Полученное видео", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
client_socket.close()
cv2.destroyAllWindows()
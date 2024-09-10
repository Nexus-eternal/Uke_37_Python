import cv2
import socket
import threading
import os

def send_video_list(client_socket):
    video_files = os.listdir("video_repository")
    video_list = "\n".join([f"{i+1}: {video}" for i, video in enumerate(video_files)])
    client_socket.sendall(video_list.encode())

def handle_client(client_socket, addr):
    send_video_list(client_socket)

    selected_video_index = int(client_socket.recv(1024).decode())
    video_files = os.listdir("video_repository")

    if selected_video_index < 1 or selected_video_index > len(video_files):
        print(f"Invalid video selection from {addr}.")
        client_socket.sendall(b"ERROR: Invalid selection")
        return

    selected_video = video_files[selected_video_index - 1]
    video_path = os.path.join("video_repository", selected_video)

    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        _, img_encoded = cv2.imencode('.jpg', frame)
        img_bytes = img_encoded.tobytes()

        client_socket.sendall(len(img_bytes).to_bytes(4, byteorder='big'))
        client_socket.sendall(img_bytes)

    cap.release()

    print(f"Video '{selected_video}' has been streamed to {addr}")
    client_socket.sendall(b"END_STREAM")

    client_socket.close()



def serve():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)

    print("Server is listening...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established.")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

    server_socket.close()

if __name__ == "__main__":
    serve()
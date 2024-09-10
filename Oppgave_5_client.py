import cv2
import socket
import numpy as np

def receive_stream(client_socket):
    print("Available videos:")
    video_list = client_socket.recv(1024).decode()
    print(video_list)

    selected_video_index = input("Enter the number of the video you want to stream: ")
    client_socket.sendall(selected_video_index.encode())

    print("Streaming video...")

    while True:
        try:
            frame_size = int.from_bytes(client_socket.recv(4), byteorder='big')
            if frame_size == 0:
                print("End of video stream.")
                break
            
            img_bytes = b''
            while len(img_bytes) < frame_size:
                packet = client_socket.recv(frame_size - len(img_bytes))
                if not packet:
                    break
                img_bytes += packet

            nparr = np.frombuffer(img_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            cv2.imshow('Client Video Stream', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except ConnectionAbortedError:
            print("Connection closed by server")
            break

    cv2.destroyAllWindows()
    client_socket.close()

if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('11.22.33.44', 12345))

    receive_stream(client_socket)
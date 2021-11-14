from socket import *
import cv2 as cv
import numpy as np

def show_image(image):
    image = np.asarray(bytearray(image), np.uint8)
    image = cv.imdecode(image, cv.IMREAD_COLOR)
    cv.imshow('image', image)
    cv.waitKey(0)


server_name = 'localhost'
server_port = 7777
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_name, server_port))

# client_socket.send(b'get_image')
# frame = client_socket.recv(1024*10000)
# show_image(frame)

client_socket.send(b'get_video')
while True:
    frame = client_socket.recv(1024*10000)

    if frame == b'end':
        break

    print('recebido')
    show_image(frame)

client_socket.close()

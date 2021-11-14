from socket import *
import cv2 as cv
import numpy as np
import time as tm

def load_image() -> bytearray:
    image = cv.imread('imagem.png')
    encoded_image = cv.imencode('.png', image)[1]
    image_array = np.array(encoded_image)
    string = image_array.tostring()

    return string

def load_video(socket) -> bytearray:
    video = cv.VideoCapture('video.3gp')

    while video.isOpened():
        ret, frame = video.read()

        if not ret:
            socket.send(b'end')
            break

        encoded_frame = cv.imencode('.png', frame)[1]
        image_array = np.array(encoded_frame)
        string = image_array.tostring()

        socket.send(string)
        tm.sleep(0.033)
    
    video.release()


server_port = 8080
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('localhost', server_port))
server_socket.listen(1)
print('Servidor pronto para receber.')


while True:
    connection_socket, address = server_socket.accept()
    sentence = connection_socket.recv(1024)

    if sentence.decode() == 'get_image':
        image = load_image()
        connection_socket.send(load_image())

    if sentence.decode() == 'get_video':
        load_video(connection_socket)

    connection_socket.close()
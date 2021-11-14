from socket import *
import cv2 as cv
import numpy as np
import time as tm

class ServerSocket:
    def __init__(self, name='localhost', port=7777) -> None:
        self.setup_socket(name, port)

    def setup_socket(self, name, port):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((name, port))
        self.socket.listen(1)
        print('Servidor pronto para receber.')
        

    def run_socket(self) -> None:
        connection_socket, address = self.socket.accept()
        sentence = connection_socket.recv(1024)

        if sentence.decode() == 'get_image':
            self.load_image(connection_socket)

        if sentence.decode() == 'get_video':
            self.load_video(connection_socket)

        connection_socket.close()


    def load_image(self, socket=None, image_name='source/imagem.png') -> None:
        if socket == None:
            socket = self.socket

        name, extension = image_name.split('.')
        image = cv.imread(image_name)
        encoded_image = cv.imencode('.'+extension, image)[1]
        image_array = np.array(encoded_image)
        string = image_array.tostring()

        socket.send(string)

    def load_video(self, socket=None, video_name='source/video.mp4') -> None:
        if socket == None:
            socket = self.socket

        video = cv.VideoCapture(video_name)

        while video.isOpened():
            ret, frame = video.read()

            if not ret:
                socket.send(b'end')
                break

            encoded_frame = cv.imencode('.jpg', frame)[1]
            image_array = np.array(encoded_frame)
            string = image_array.tostring()

            socket.send(string)
            tm.sleep(0.016)
        
        video.release()



if __name__ == '__main__':
    socket = ServerSocket('localhost', 7777)
    
    while True:
        socket.run_socket()
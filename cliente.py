from socket import *
import cv2 as cv
import numpy as np
import os
import time as tm

class ClientSocket:
    def __init__(self, name='localhost', port=7777) -> None:
        self.setup_socket(name, port)

    def setup_socket(self, name, port) -> None:
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((name, port))
    
    def get_image(self):
        print('Obtendo imagem...')
        self.socket.send(b'get_image')

        frame = self.socket.recv(1024*10000)
        print('Exibindo imagem...')
        self.show_image(frame, 0)

        self.socket.close()
        print('Finalizado.')

    def get_video(self):
        print('Obtendo video...')
        self.socket.send(b'get_video')

        print('Reproduzindo video...')
        while True:
            frame = self.socket.recv(1024*10000)

            if frame == b'end':
                break

            self.show_image(frame, 1)

        cv.destroyAllWindows()
        self.socket.close()
        print('Finalizado.')

    def get_whole_video(self):
        print('Obtendo video...')
        self.socket.send(b'get_whole_video')
        bn_video = self.socket.recv(7925885)

        temp_addr = 'temp_video.mp4'
        with open(temp_addr, 'wb') as video:
            video.write(bn_video)

        print('Reproduzindo video...')
        video = cv.VideoCapture(temp_addr)

        while video.isOpened():
            ret, frame = video.read()

            if not ret:
                break

            cv.imshow('frame', frame)
            cv.waitKey(1)

            tm.sleep(0.016)
        
        video.release()


        cv.destroyAllWindows()
        self.socket.close()
        print('Finalizado.')

    def show_image(self, image, key=0):
        image = np.asarray(bytearray(image), np.uint8)
        image = cv.imdecode(image, cv.IMREAD_COLOR)
        cv.imshow('image', image)
        cv.waitKey(key)


if __name__ == '__main__':
    choice = None

    while choice != '0':
        os.system('cls')
        print('------------')
        print('1- Imagem')
        print('2- Video streaming')
        print('3- Video inteiro')
        print('0- Cancelar')
        print('------------\n')

        choice = input('Selecione uma opção: ')

        if choice == '1':
            client_socket = ClientSocket('localhost', 7777)
            client_socket.get_image()

        elif choice == '2':
            client_socket = ClientSocket('localhost', 7777)
            client_socket.get_video()
        
        elif choice == '3':
            client_socket = ClientSocket('localhost', 7777)
            client_socket.get_whole_video()

            









from socket import *
import cv2 as cv
import numpy as np
import os

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

    def show_image(self, image, key=0):
        image = np.asarray(bytearray(image), np.uint8)
        image = cv.imdecode(image, cv.IMREAD_COLOR)
        cv.imshow('image', image)
        cv.waitKey(key)




if __name__ == '__main__':
    choice = None

    while choice != '3':
        os.system('cls')
        print('------------')
        print('1- Imagem')
        print('2- Video')
        print('3- Cancelar')
        print('------------\n')

        choice = input('Selecione uma opção: ')

        if choice == '1':
            client_socket = ClientSocket('localhost', 7777)
            client_socket.get_image()

        elif choice == '2':
            client_socket = ClientSocket('localhost', 7777)
            client_socket.get_video()









from socket import *
import cv2 as cv
import numpy as np
import time as tm
import pickle as pc
import struct as st
import sys

class ServerSocket:
    '''
    Server Socket class. Sends imagens or videos to a client.
    '''


    def __init__(self, name='localhost', port=7777) -> None:
        self.setup_socket(name, port)

    def setup_socket(self, name, port):
        '''
        Sets up the socket.
        '''

        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((name, port))
        self.socket.listen(1)
        print('Servidor pronto para receber.')
        
    def run_socket(self) -> None:
        '''
        Runs socket connection.
        '''

        connection_socket, address = self.socket.accept()
        sentence = connection_socket.recv(1024)

        if sentence.decode() == 'get_image':
            self.load_image(connection_socket)

        if sentence.decode() == 'get_video':
            self.load_video(connection_socket)

        if sentence.decode() == 'get_whole_video':
            self.load_whole_video(connection_socket)

        connection_socket.close()

    def load_image(self, socket=None, image_name='source/imagem.png') -> None:
        '''
        Sends an image to the client using a socket.
        '''

        if socket == None:
            socket = self.socket

        # carrega a imagem
        image = cv.imread(image_name)

        # serializa os dados e calcula o tamanho
        data = pc.dumps(image)
        message_size = st.pack('L', len(data))

        # envia o tamanho da mensagem e os dados
        socket.sendall(message_size + data)

    def load_video(self, socket=None, video_name='source/video.mp4') -> None:
        '''
        Streams a video to the client using a socket.
        '''

        if socket == None:
            socket = self.socket

        # carrega o video
        video = cv.VideoCapture(video_name)

        while True:
            # le um quadro do video
            ret, frame = video.read()

            # caso ret seja falso, o video finalizou
            if not ret:
                data = pc.dumps(b'end')
                message_size = st.pack('L', len(data))
                socket.sendall(message_size + data)
                break
            
            # serializa os dados e calcula o tamanho
            data = pc.dumps(frame)
            message_size = st.pack('L', len(data))

            # envia o tamanho da mensagem e os dados
            socket.sendall(message_size + data)

            # pausa para sincronizar os frames
            tm.sleep(0.016)

        video.release()


if __name__ == '__main__':
    socket = ServerSocket('localhost', 7777)
    
    while True:
        socket.run_socket()
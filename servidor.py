from socket import *
import cv2 as cv
import time as tm
import pickle as pc
import struct as st

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
            self.load_image(address, connection_socket)

        if sentence.decode() == 'get_video':
            self.load_video(connection_socket)

        connection_socket.close()

    def load_image(self, address, socket=None, image_name='source/imagem.jpg') -> None:
        '''
        Sends an image to the client using a socket.
        '''

        if socket == None:
            socket = self.socket

        # carrega a imagem
        image = cv.imread(image_name)

        # serializa os dados e calcula o tamanho
        data = pc.dumps(image)
        message_size = st.pack('i', len(data))

        # envia o tamanho da mensagem e os dados
        print('Enviando imagem...')
        socket.sendall(message_size + data)
        print('Mensagem enviada.')

    def load_video(self, socket=None, video_name='source/video.mp4') -> None:
        '''
        Streams a video to the client using a socket.
        '''

        if socket == None:
            socket = self.socket

        # carrega o video
        video = cv.VideoCapture(video_name)

        print('Transmitindo video...')
        
        while True:
            # le um quadro do video
            ret, frame = video.read()

            # caso ret seja falso, o video finalizou
            if not ret:
                data = pc.dumps(b'end')
                message_size = st.pack('i', len(data))
                socket.sendall(message_size + data)
                break
            
            # serializa os dados e calcula o tamanho
            data = pc.dumps(frame)
            message_size = st.pack('i', len(data))

            # envia o tamanho da mensagem e os dados
            socket.sendall(message_size + data)

            # pausa para sincronizar os frames
            tm.sleep(0.033)

        print('Video transmitido.')

        video.release()


if __name__ == '__main__':
    socket = ServerSocket('', 7777)
    
    while True:
        socket.run_socket()
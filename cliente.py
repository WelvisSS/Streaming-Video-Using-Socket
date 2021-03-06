import pickle as pc
from socket import *
import cv2 as cv
import os
import struct as st

class ClientSocket:
    '''
    Client Socket class. Receives images or videos from a server.
    '''

    def __init__(self, name='localhost', port=7777) -> None:
        self.setup_socket(name, port)

    def setup_socket(self, name, port) -> None:
        '''
        Sets up the socket.

        Parameters:
            - name (string): server name/adress on the network
            - port (int): port of the server
        '''

        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((name, port))
    
    def get_image(self) -> None:
        '''
        Gets an image from a server.
        '''

        print('Obtendo imagem...')
        self.socket.send(b'get_image')

        # estabelece o tamanho do lote
        data = b''
        payload_size = st.calcsize('i')
        
        # recebe dados enquanto não atingir o tamanho do lote
        while len(data) < payload_size:
            data += self.socket.recv(1024*100)

        # separa o tamanho do frame dos dados recebidos
        packed_message_size = data[:payload_size]
        data = data[payload_size:]
        message_size = st.unpack('i', packed_message_size)[0]

        # recebe mais dados enquanto não atingir o tamanho da mensagem
        while len(data) < message_size:
            data += self.socket.recv(1024*100)


        # separa os dados do frame
        image_data = data[:message_size]
        data = data[message_size:]

        # desserializa os dados
        image = pc.loads(image_data)

        # mostra a imagem
        print('Exibindo imagem...')
        cv.imshow('imagem', image)
        cv.waitKey(0)

        self.socket.close()
        print('Finalizado.')

    def get_video(self) -> None:
        '''
        Gets a video from a server.
        '''

        print('Solicitando video...')

        self.socket.send(b'get_video')

        print('Reproduzindo video...')

        # estabelece o tamanho do lote
        data = b''
        payload_size = st.calcsize('i')
        
        while True:
            # recebe dados enquanto não atingir o tamanho do lote
            while len(data) < payload_size:
                data += self.socket.recv(1024*100)

            # separa o tamanho do frame dos dados recebidos
            packed_message_size = data[:payload_size]
            data = data[payload_size:]
            message_size = st.unpack('i', packed_message_size)[0]

            # recebe mais dados enquanto não atingir o tamanho da mensagem
            while len(data) < message_size:
                data += self.socket.recv(1024*100)

            # separa os dados do frame
            frame_data = data[:message_size]
            data = data[message_size:]

            # desserializa os dados
            frame = pc.loads(frame_data)

            # finaliza se receber um b'end'
            if frame == b'end':
                break

            # mostra o frame
            cv.imshow('Stream', frame)
            cv.waitKey(1)

        # destroi as janelas e fecha o soquete
        cv.destroyAllWindows()
        self.socket.close()
        
        print('Finalizado.')


if __name__ == '__main__':
    choice = None

    while choice != '0':
        # os.system('cls')
        print('------------')
        print('1- Imagem')
        print('2- Video streaming')
        print('0- Cancelar')
        print('------------\n')

        choice = input('Selecione uma opção: ')

        client_socket = ClientSocket('192.168.0.200', 7777)
        if choice == '1':
            client_socket.get_image()

        elif choice == '2':
            client_socket.get_video()


            









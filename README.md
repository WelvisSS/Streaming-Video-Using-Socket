# Streaming de Vídeo Usando Socket
#### Curso: Ciência da Computação
#### Trablho de Rede de Computadores I
#### Professor: Jorge Lima de Oliveira Filho
#### Desenvolvedores: Fabiano Silva dos Santos, Welvis Silva Souza.

# Servidor

### Bibliotecas utilizadas:
```
from socket import *
import cv2 as cv
import time as tm
import pickle as pc
import struct as st
```
- A biblioteca socket é a biblioteca que possibilita a conexão e criação dos sockets, além do envia dos dados entre cliente e servidor. 
```
from socket import *
```
- A biblioteca cv2 é utilizada para processamento de imagem.
```
import cv2 as cv
```
- A biblioteca time é utilizada para cálculo de tempo.
```
import time as tm
```
- A biblioteca pickle implementa protocolos binários para serializar e desserializar uma estrutura de objeto Python.
```
import pickle as pc
```
- A biblioteca struct serve faz a conversão entre structs de C e valores de Python, representados por objetos bytes em Python.
```
import struct as st
```

### Classe de envio de imagens e vídeos para clientes.
```
class ServerSocket:
```
### Inicializador da classe ServerSocket:
#### Função:
- Inicializa o nome do host e a porta que o servidor irá rodar. 
- O host pode ser alterado pelo ip da máquina possibilitando conexão entre outros dispositivos.
#### Parametros:
- name (string): host de conexão
- port (int): porta utilizada

```
def __init__(self, name='localhost', port=7777) -> None:
    self.setup_socket(name, port)
```
### Método setup_socket:

#### Função:
- Inicializa as configurações do socket com um protocolo do tipo TCP.

#### Parametros:
- nome (string): Nome do host
- port (int): Porta que será utilizada

```
def setup_socket(self, name, port):
    '''
    Sets up the socket.
    '''
    self.socket = socket(AF_INET, SOCK_STREAM)
    self.socket.bind((name, port))
    self.socket.listen(1)
    print('Servidor pronto para receber.')
```
### Método run_socket:
#### Função:
- Aceita a conexão do cliente.
- Recebe uma mensagem do cliente. 
- Com base na mensagem passada pelo cliente chama um método correspondente do servidor.

```
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
```
### Método load_image:
#### Função:
- Abre a imagem utilizando o openCV
- Faz a serialização da imagem, calculando o tamanho que a mesma possui.
- Faz o envio do tamanho da imagem juntamente com os dados que foram serializados.
#### Parametros:
- address (string): Endereço de conexão
- socket (socket): Tipo de conexão
- image_name (string): Caminho da imagem
  

```
def load_image(self, address, socket=None, image_name='source/imagem.png') -> None:
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
```
### Método load_video:

#### Função:
- Faz o carregamento do vídeo
- Faz a leitura de quadro por quadro do vídeo
- Faz a serialização de cada quadro enviando o tamanho do quadro e a imagem correspondente
- Utiliza o time para adicionar uma pausa para sincronizar os frames deixando os cortes com características de vídeo.
#### Parametros:
- socket (socket): Tipo de conexão
- video_name (string): Caminho do vídeo


```
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
        tm.sleep(0.016)

    print('Video transmitido.')

    video.release()
```
### Instância a classe, e executa o método run_socket 
```
if __name__ == '__main__':
    socket = ServerSocket('', 7777)
    
    while True:
        socket.run_socket()
```


# Cliente

### Bibliotecas utilizadas:
```
import pickle as pc
from socket import *
import cv2 as cv
import struct as st
```

- A biblioteca pickle implementa protocolos binários para serializar e desserializar uma estrutura de objeto Python.
```
import pickle as pc
```
- A biblioteca socket é a biblioteca que possibilita a montagem do socket. 
```
from socket import *
```
- A biblioteca cv2 é utilizada para processamento de imagem.
```
import cv2 as cv
```
- A biblioteca struct serve para interpretar bytes como um pacote de dados binários.
```
import struct as st
```

### Recebe as imagens e vídeos enviados pelo servidor.
```
class ClientSocket:
```

### Inicializador da classe ClientSocket:
#### Função:
- Inicializa o nome do host e a porta que o servidor irá rodar. 
- O host pode ser alterado pelo ip da máquina possibilitando conexão entre outros dispositivos.
#### Parametros:
- name (string): host de conexão
- port (int): porta utilizada

```
def __init__(self, name='localhost', port=7777) -> None:
        self.setup_socket(name, port)
```
### Método setup_socket:

#### Função:
- Inicializa as configurações do socket com um protocolo do tipo TCP.

#### Parametros:
- nome (string): Nome do host
- port (int): Porta que será utilizada

```
 def setup_socket(self, name, port) -> None:
    '''
    Sets up the socket.
    '''

    self.socket = socket(AF_INET, SOCK_STREAM)
    self.socket.connect((name, port))
```
### Método get_image:

#### Função:
- Recebe as imagens vindas direto do servidor.
- Estabelece o tamanho do lote.
- Separa o tamanho dos dados recebidos.
- Desserializa os dados recebidos.
- Monta a imagem.


```
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
```

### Método get_video:

#### Função:
- Estabelece o tamanho do lote.
- Faz a separação de cada frame dos dasdos recebidos.
- Desserializa os dados.
- Mostra o frame.

```
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
```

### Instânciação da classe
- Menu com as opções de serviços de imagem e vídeo que o usuário pode executar
- Executa o método client_socket com a entrada pré definida pelo usuário

```
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
```

# Eventos, Estados e Mensagens:
#### Os eventos, estados e mensagens por trás de toda a lógica do código estão funcionando da seguinte maneira:

<br />
<div style="line-height: 2;">
    <ol>
        <li>Servidor se prepara e aguarda solicitações - o servidor é criado, e é preparado na rede local, com nome 'localhost' porta padrão 7777 e a partir daí fica no aguardo de novas solicitações;</li>
        <li>Cliente solicita conexão - o cliente envia ao servidor uma solicitação de conexão do socket para iniciar as interações;
        </li>
        <li>Servidor aceita a conexão - o servidor aceita a conexão solicitada pelo cliente e espera a solicitação do que fazer em seguida;
        </li>
        <li>Servidor aguarda solicitações de conteúdo - o servidor começa a aguardar que o cliente que estabeleceu a conexão envie uma solicitação sobre qual conteúdo deseja;
        </li>
        <li>Cliente solicita um conteúdo ao servidor - o cliente envia uma solicitação para o servidor para começar a receber um determinado conteúdo entre dois tipos de conteúdos possíveis;
            <ul>
                <li> a. Cliente solicita imagem - no caso de solicitação de imagem, o cliente envia um 'get_image' para o servidor; 
                    <ul>
                        <li>i. Servidor recebe a solicitação do conteúdo - o servidor decodifica a mensagem enviada pelo cliente e entende que deve enviar a imagem;</li>
                        <li>ii. Servidor envia a imagem - o servidor começa a enviar o tamanho dos pacotes e os dados da imagem até que não tenha mais dados para enviar;</li>
                        <li>iii. Cliente recebe dados da imagem - o cliente recebe todos os dados e decodifica, depois mostra na tela a imagem que recebeu do servidor.</li>
                    </ul>
                </li>            
                <li>b. Cliente solicita vídeo - no caos de solicitação de video, o cliente envia um 'get_video' para o servidor;
                    <ul>
                        <li>i. Servidor recebe a solicitação do conteúdo - o servidor decodifica a mensagem enviada pelo cliente e entende que deve enviar o video;</li>
                        <li>ii. Servidor envia o video - o servidor começa a enviar o video que foi solicitado pelo cliente até que não haja mais dados;
                            <ul>
                                <li>1) Servidor envia o frame do vídeo - o servidor começa a enviar o tamanho dos pacotes de cada quadro e o quadro o video até que não tenha mais dados;</li>
                                <li>2) Cliente recebe  o frame e mostra - o cliente recebe um quadro do servidor e o mostra logo em seguida, e em seguida se prepara para receber o próximo quadro.</li>
                            </ul>
                        </li>
                        <li>iii. Servidor envia sinal de final do video - o servidor envia um 'end' para o cliente, indicando que o video acabou e não há mais dados para enviar.</li>
                    </ul>
                </li>
                <li> c. Cliente cancela solicitação - ao cancelar a solicitação o programa finaliza o socket e o programa cliente fecha; 
                </li> 
            </ul>
        </li>
        <li>Servidor fecha o socket do cliente - o servidor fecha a conexão com o socket do cliente, visto que não há mais dados para serem enviados;
        </li>
        <li>Cliente fecha o socket - o cliente fecha o socket visto que todo o processo foi finalizado.
        </li>
    </ol>
</div>

<br />

# Diagrama:
![img](https://raw.githubusercontent.com/WelvisSS/Streaming-Video-Using-Socket/main/Demonstra%C3%A7%C3%A3o/Estados.png)


# Funcionamento do software:
O programa desenvolvido faz a tranferência de imagens ou o streaming de vídeos atrvéz de um socket TCP, entre cliente e servidor. O usuário tem a possibilidade de escolher entre transferência de imagem e vídeo. Após a escolha do usuário onde a conexão já está sendo estabelecida, é feita a troca de informações cliente e servidor de modo que haja uma tranferêcia de imagem ou vídeo. O servidor envia imagem ou o vídeo que estão armazenados em pasta local para cliente. Após receber os dados o cliente reproduz imagem ou vídeo.

# Propósito do software:
O propósito so software é transferir imagens ou vídeos através de streaming de um servidor para um cliente.

# Motivação da escolha do protocolo de transporte:
O protocolo escolhido foi o TCP, sendo escolhido por conta de garantir maior integradade de transferência de imagens e vídeos, fazendo com que os dados transferidos cheguem sem nehum tipo de perda.

# Requisitos mínimos de funcionamento:
- Rede local 
- Máquina com python 3.7 
- OpenCV: pip install opencv-python
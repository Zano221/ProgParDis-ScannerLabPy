import socket
import mysql.connector
from PIL import Image, ImageChops
import io

#configuração de servidor
server_ip = '127.0.0.1'
server_port = 1337

# Criação de socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

## Carregar as imagens de cientistas presentes
image_reference = Image.open('C:\Add1.jpg')

same_images = True

try:
    #Vincular o endereço IP e porta ao socket
    server_socket.bind((server_ip, server_port))

    server_socket.listen(1)

    while True:
        print("Servidor pronto para receber conexões")
        client_socket, client_address = server_socket.accept()
        print("Conexão estabelecida com:", client_address)

        #Recebendo mensagem do cliente
        print("Escutando...")
        message = client_socket.recv(300000)

        print("Imagem Recebida")

        #Determinar se a imagem existe
        print("Comparando as duas imagens")
        received_image = Image.open(io.BytesIO(message))

        if received_image.size != image_reference.size:
            same_images = False
        else:
            difference = ImageChops.difference(received_image, image_reference)
            if difference.getbbox():
                same_images = False

        #Se ela existe, checa a permissão dele no setor
        if same_images:
            result = "IGUAIS"
        else:
            result = "DIFERENTES"
        
        client_socket.sendall(result.encode())
        #Transformação da string em letras maíusculas

        client_socket.close()
        print("Conexão encerrada com:", client_address)

finally:
    #Encerrando o socket do servidor
    server_socket.close()

        


import socket
from tkinter import filedialog


def open_image():
    path = filedialog.askopenfilename(title="Selecione a sua imagem", initialdir=".\\images_cli\\")
    with open(path, 'rb') as image:
        return image.read()

#configuração de servidor
server_ip = '127.0.0.1'
server_port = 1337

# Criação de socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    #Conexão com o servidor
    client_socket.connect((server_ip, server_port))

    #Abrir imagem para mandar ao servidor
    image = open_image()
    if image is None:
        print("TEM Q TE IMAGE HAMILTON")
        exit()

    message = input("Digite a sua mensagem: ")

    client_socket.sendall(image)

    #enviar a menssagem do setor
    client_socket.sendall(message.encode())

    print("Esperando por resposta...")
    modified_message = client_socket.recv(1024).decode()

    print("As images são iguais?: ", modified_message)    
except ConnectionRefusedError:
    print("Erro ao comunicar com o servidor")

finally:
    client_socket.close()
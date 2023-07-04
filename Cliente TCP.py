import socket


#configuração de servidor
server_ip = '127.0.0.1'
server_port = 1337

# Criação de socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    #Conexão com o servidor
    client_socket.connect((server_ip, server_port))

    message = input("Digite a sua mensagem: ")
    #client_socket.sendall(message.encode())

    image = open('imagem_recebida.jpg', 'rb')
    raw_image = image.read()
    image.close()

    client_socket.sendall(raw_image)

    print("Esperando por resposta...")
    modified_message = client_socket.recv(1024).decode()

    print("As images são iguais?: ", modified_message)    
except ConnectionRefusedError:
    print("Erro ao comunicar com o servidor")

finally:
    client_socket.close()
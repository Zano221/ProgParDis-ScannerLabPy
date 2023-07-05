import socket, io, os
from PIL import Image, ImageChops

#configuração de servidor
server_ip = '127.0.0.1'
server_port = 1337

# Criação de socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

## Carregar as imagens dos cientistas

image_db = []
path = os.path.abspath('.\images')
if path is None:
    print("ERRO! Deve existir um diretorio das imagens 'images'! ")
image_paths = os.listdir(path)

#Vo adicionar uma função que escolhe aleatoriamente entre A e E mas vou deixar pra dps
array_of_letters = ['A', 'B', 'C', 'D', 'E']
_key = 0
for p in image_paths:
    if _key > 4:
        _key = 0
    image_db.append((Image.open('.\images\\' + p), array_of_letters[_key]))
    print(".\images\\" + p, array_of_letters[_key])
    _key += 1

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

        print("Recebendo setor...")
        sector_message = client_socket.recv(1024).decode()

        #Autenticar Cientista
        print("Comparando a imagem recebida com as do banco de dados")

        received_image = Image.open(io.BytesIO(message))

        #Loopar pelo banco de dados das imagens do servidor
        for i in image_db:
            difference = ImageChops.difference(received_image, i[0])
            #Determinar se a imagem existe
            if not difference.getbbox():      
                print("É A IMAGEM DO", i[1])
                #Determinar se o Cientista está acessando o setor correto
                if i[1] != sector_message.upper():
                    result = "CIENTISTA NÃO TEM PERMISSÃO PARA ACESSAR O SETOR " + i[1]
                    break
                result = "SEJA BEM VINDO AO SETOR " + i[1]
                break
            else:
                result = "CIENTISTA NÃO EXISTE!"
                
        #Enviar resultado final de permissão ao cientista
        client_socket.sendall(result.encode())
        #Transformação da string em letras maíusculas

        client_socket.close()
        print("Conexão encerrada com:", client_address)

finally:
    #Encerrando o socket do servidor
    server_socket.close()

        


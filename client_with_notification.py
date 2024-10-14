import socket

def start_client(image_path):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 9090))
    
    # Enviando o caminho da imagem ao servidor
    client.send(image_path.encode('utf-8'))
    
    # Recebendo status do processamento
    while True:
        response = client.recv(1024).decode('utf-8')
        if not response:
            break
        print(f"Server: {response}")
    
    client.close()

if __name__ == "__main__":
    # Substitua 'image1.png' com o nome da imagem que deseja processar
    start_client('image2.jpg')

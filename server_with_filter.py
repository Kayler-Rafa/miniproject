import socket
import threading
import time
from PIL import Image, ImageFilter
import os

# Variável global para rastrear o número de imagens processadas
images_queue = []
image_processing_status = {}

# Função para processar imagens
def process_image(image_path, client_socket, client_id):
    try:
        print(f"Processing {image_path} for Client {client_id}...")
        
        # Verificando se o arquivo existe
        if not os.path.exists(image_path):
            print(f"Error: {image_path} not found.")
            client_socket.send(f"Error: {image_path} not found.".encode('utf-8'))
            return
        
        # Abrindo e aplicando filtro
        image = Image.open(image_path)
        filtered_image = image.filter(ImageFilter.GaussianBlur(5))  # Exemplo de filtro
        
        # Convertendo para RGB, se necessário
        if filtered_image.mode == 'RGBA':
            filtered_image = filtered_image.convert('RGB')
        
        output_path = f"processed_{client_id}.jpg"
        filtered_image.save(output_path)
        
        # Atualizando status de processamento
        image_processing_status[client_id] = f"Processed image {client_id}"

        # Notificando o cliente sobre a conclusão do processamento
        client_socket.send(f"Your image has been processed: {output_path}".encode('utf-8'))
        client_socket.close()

    except Exception as e:
        client_socket.send(f"An error occurred: {e}".encode('utf-8'))
        client_socket.close()

# Função para lidar com clientes e manter a fila de imagens
def handle_client(client_socket, address, client_id):
    print(f"Connection from {address} (Client {client_id})")
    
    # Recebendo o nome do arquivo de imagem do cliente
    image_path = client_socket.recv(1024).decode('utf-8')
    print(f"Client {client_id} is sending image: {image_path}")
    
    # Adicionando à fila de processamento
    images_queue.append((image_path, client_id))
    print(f"Added image {image_path} from Client {client_id} to the queue.")
    
    # Notificando o cliente sobre o status atual
    queue_position = len(images_queue)
    client_socket.send(f"Currently processing image {images_queue[0][1]}. Your image is at position {queue_position}.".encode('utf-8'))
    
    # Processando a imagem do cliente
    process_image(image_path, client_socket, client_id)

# Servidor para receber e processar as imagens
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9090))
    server.listen(5)
    print("Server listening on port 9090...")
    
    client_id = 0  # Identificador único para cada cliente

    while True:
        client_socket, address = server.accept()
        client_id += 1
        # Criando uma thread para lidar com o cliente
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address, client_id))
        client_thread.start()

if __name__ == "__main__":
    start_server()

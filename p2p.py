import socket
import threading

# Função para lidar com conexões recebidas
def handle_incoming_connections(peer_socket):
    while True:
        client_socket, address = peer_socket.accept()
        print(f"Received connection from {address}")
        message = client_socket.recv(1024).decode('utf-8')
        print(f"Message from {address}: {message}")
        client_socket.send(f"Hello from Node!".encode('utf-8'))
        client_socket.close()

# Função para conectar a outro nó
def connect_to_peer(peer_address, peer_port):
    peer_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer_client.connect((peer_address, peer_port))
    peer_client.send("Hello from another Node!".encode('utf-8'))
    response = peer_client.recv(1024).decode('utf-8')
    print(f"Response from peer: {response}")
    peer_client.close()

# Função principal para o nó P2P
def start_peer(port):
    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer_socket.bind(('0.0.0.0', port))  # Porta para escutar as conexões
    peer_socket.listen(5)
    print(f"Node is listening on port {port}...")

    # Thread para lidar com conexões recebidas
    threading.Thread(target=handle_incoming_connections, args=(peer_socket,)).start()

# Iniciar o nó P2P
if __name__ == "__main__":
    # Inicializando o nó P2P na porta 9092
    start_peer(9092)

    # Conectando-se a outro nó
    connect_to_peer('localhost', 9092)

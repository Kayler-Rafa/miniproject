import socket
import threading

# Função para lidar com a conexão de cada cliente
def handle_client(client_socket, address, connection_count):
    print(f"Connection from {address} established.")
    # Receber mensagem do cliente
    message = client_socket.recv(1024).decode('utf-8')
    print(f"Received from {address}: {message}")
    
    # Enviar resposta para o cliente
    response = f"Hello, Client! Currently handling {connection_count} connections."
    client_socket.send(response.encode('utf-8'))
    
    # Fechar conexão
    client_socket.close()

# Configurando o servidor
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9090))  # Mudando para a porta 9090
    server.listen(5)  # Permite até 5 conexões na fila
    print("Server is listening on port 9090...")
    
    connection_count = 0
    
    while True:
        client_socket, address = server.accept()
        connection_count += 1
        # Criando uma nova thread para cada cliente
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address, connection_count))
        client_thread.start()

# Iniciar o servidor
if __name__ == "__main__":
    start_server()

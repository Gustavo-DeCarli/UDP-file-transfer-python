from socket import *
import time
import os

# Configurações do servidor
serverPort = 12000
bufferSize = 65535  # tamanho máximo do pacote UDP
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("", serverPort))

print(f"Servidor UDP iniciado na porta {serverPort}")
print("Aguardando arquivo do cliente...")

while True:
    # Recebe nome do arquivo
    file_info, clientAddress = serverSocket.recvfrom(bufferSize)
    filename = file_info.decode()
    print(f"Recebendo arquivo: {filename}")
    serverSocket.sendto("OK".encode(), clientAddress)

    # Recebe tamanho total do arquivo
    file_size_data, _ = serverSocket.recvfrom(bufferSize)
    total_size = int(file_size_data.decode())
    print(f"Tamanho total: {total_size} bytes")
    serverSocket.sendto("OK".encode(), clientAddress)

    # Cria arquivo para escrita
    with open("recebido_" + os.path.basename(filename), "wb") as f:
        received_bytes = 0
        packet_count = 0
        start_time = time.time()

        while received_bytes < total_size:
            data, _ = serverSocket.recvfrom(bufferSize)
            if data == b"EOF":
                break
            f.write(data)
            received_bytes += len(data)
            packet_count += 1

        end_time = time.time()

    print("\n📦 Transferência concluída!")
    print(f"Arquivo salvo como: recebido_{filename}")
    print(f"Tamanho recebido: {received_bytes} bytes")
    print(f"Número de pacotes: {packet_count}")
    print(f"Duração: {end_time - start_time:.2f} segundos")
    if end_time - start_time > 0:
        print(f"Taxa média: {received_bytes / (end_time - start_time):.2f} bytes/s\n")

    # Aguarda próximo arquivo
    print("Aguardando próximo arquivo...\n")

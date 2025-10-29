from socket import *
import os
import time

serverName = input("Digite o endereço IP do servidor (ex: 127.0.0.1): ")
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

filename = input("Digite o nome do arquivo a ser enviado: ")

if not os.path.exists(filename):
    print("Arquivo não encontrado!")
    clientSocket.close()
    exit()

packet_size = int(input("Digite o tamanho do pacote (em bytes): "))

# Envia nome do arquivo
clientSocket.sendto(filename.encode(), (serverName, serverPort))
clientSocket.recvfrom(1024)

# Envia tamanho total do arquivo
file_size = os.path.getsize(filename)
clientSocket.sendto(str(file_size).encode(), (serverName, serverPort))
clientSocket.recvfrom(1024)

print(f"Iniciando envio de '{filename}' ({file_size} bytes)...")

# Envia conteúdo do arquivo
start_time = time.time()
with open(filename, "rb") as f:
    bytes_sent = 0
    packet_count = 0

    while True:
        data = f.read(packet_size)
        if not data:
            break
        clientSocket.sendto(data, (serverName, serverPort))
        bytes_sent += len(data)
        packet_count += 1

# Envia fim de arquivo
clientSocket.sendto(b"EOF", (serverName, serverPort))
end_time = time.time()

print("\n✅ Envio concluído!")
print(f"Tamanho enviado: {bytes_sent} bytes")
print(f"Número de pacotes: {packet_count}")
print(f"Duração: {end_time - start_time:.2f} segundos")
if end_time - start_time > 0:
    print(f"Taxa média: {bytes_sent / (end_time - start_time):.2f} bytes/s")

clientSocket.close()

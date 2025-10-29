from socket import *
import os
import time

serverName = input("Digite o endereço IP do servidor (ex: 127.0.0.1): ")
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(5)

# Usuário define tamanho do arquivo e nome
filename = input("Digite o nome fictício do arquivo (ex: teste.bin): ")
fake_size = int(input("Digite o tamanho do arquivo fictício em bytes: "))
packet_size = int(input("Digite o tamanho do pacote (em bytes): "))

# Gerar conteúdo fictício (só texto repetido ou bytes)
fake_data = b"A" * fake_size  # pode ser qualquer padrão de byte

# Envia nome do arquivo
clientSocket.sendto(filename.encode(), (serverName, serverPort))
msg, _ = clientSocket.recvfrom(1024)

# Envia tamanho total do arquivo
clientSocket.sendto(str(fake_size).encode(), (serverName, serverPort))
msg, _ = clientSocket.recvfrom(1024)

print(f"Iniciando envio do arquivo fictício '{filename}' ({fake_size} bytes)...")

# Envia os dados simulados em pacotes
start_time = time.time()
bytes_sent = 0
packet_count = 0

while bytes_sent < fake_size:
    chunk = fake_data[bytes_sent:bytes_sent + packet_size]
    clientSocket.sendto(chunk, (serverName, serverPort))
    bytes_sent += len(chunk)
    packet_count += 1

    if packet_count % 100 == 0 or bytes_sent == fake_size:
        print(f"Enviado: {bytes_sent}/{fake_size} bytes ({(bytes_sent / fake_size) * 100:.1f}%)")

# Envia sinal de fim de arquivo
clientSocket.sendto(b"EOF", (serverName, serverPort))
end_time = time.time()

print("\n✅ Envio concluído!")
print(f"Tamanho enviado: {bytes_sent} bytes")
print(f"Número de pacotes: {packet_count}")
print(f"Duração: {end_time - start_time:.2f} segundos")
if end_time - start_time > 0:
    print(f"Taxa média: {bytes_sent / (end_time - start_time):.2f} bytes/s")

clientSocket.close()

from socket import *
import os
import time

serverName = input("Digite o endereço IP do servidor (ex: 127.0.0.1): ")
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(5)  # timeout para evitar travamentos

filename = input("Digite o nome do arquivo a ser enviado: ")

if not os.path.exists(filename):
    print("Arquivo não encontrado!")
    clientSocket.close()
    exit()

packet_size = int(input("Digite o tamanho do pacote (em bytes): "))

# --- Envio das informações iniciais ---
try:
    # Envia nome do arquivo
    clientSocket.sendto(filename.encode(), (serverName, serverPort))
    msg, _ = clientSocket.recvfrom(1024)
    if msg.decode() != "OK":
        print("Erro ao iniciar comunicação com o servidor.")
        clientSocket.close()
        exit()

    # Envia tamanho total do arquivo
    file_size = os.path.getsize(filename)
    clientSocket.sendto(str(file_size).encode(), (serverName, serverPort))
    msg, _ = clientSocket.recvfrom(1024)
    if msg.decode() != "OK":
        print("Erro ao enviar tamanho do arquivo.")
        clientSocket.close()
        exit()

    print(f"Iniciando envio de '{filename}' ({file_size} bytes)...")

    # --- Envio do arquivo ---
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

            # Mostra progresso simples
            if packet_count % 100 == 0 or bytes_sent == file_size:
                print(f"Enviado: {bytes_sent}/{file_size} bytes ({(bytes_sent/file_size)*100:.1f}%)")

    # Envia sinal de fim de arquivo
    clientSocket.sendto(b"EOF", (serverName, serverPort))
    end_time = time.time()

    print("\n✅ Envio concluído!")
    print(f"Tamanho enviado: {bytes_sent} bytes")
    print(f"Número de pacotes: {packet_count}")
    print(f"Duração: {end_time - start_time:.2f} segundos")
    if end_time - start_time > 0:
        print(f"Taxa média: {bytes_sent / (end_time - start_time):.2f} bytes/s")

except timeout:
    print("⏰ O servidor não respondeu. Verifique se ele está em execução e acessível.")
except Exception as e:
    print("Erro durante o envio:", e)

clientSocket.close()

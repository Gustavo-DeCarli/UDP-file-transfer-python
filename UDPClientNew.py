from socket import *
import os
import time

# Config
serverName = input("Digite o número do IP do server: ")
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

arquivo_path = input("Digite o caminho do arquivo a enviar: ").strip()
tam_pacote = int(input("Digite o tamanho de cada pacote (em bytes): "))

if not os.path.exists(arquivo_path):
    print("Arquivo não encontrado.")
    clientSocket.close()
    exit()

# Lê o arquivo em binário
with open(arquivo_path, "rb") as f:
    dados = f.read()

tamanho_total = len(dados)
num_pacotes = (tamanho_total + tam_pacote - 1) // tam_pacote

print(f"\nEnviando arquivo: {os.path.basename(arquivo_path)}")
print(f"Tamanho total: {tamanho_total} bytes")
print(f"Pacotes: {num_pacotes} de {tam_pacote} bytes cada\n")

inicio = time.time()

# Envia metadados
info = f"START|{os.path.basename(arquivo_path)}|{tamanho_total}|{num_pacotes}"
clientSocket.sendto(info.encode(), (serverName, serverPort))
ack, _ = clientSocket.recvfrom(1024)
print("Servidor pronto:", ack.decode())

# Enviar pacotes
for i in range(num_pacotes):
    inicio_byte = i * tam_pacote
    fim_byte = inicio_byte + tam_pacote
    chunk = dados[inicio_byte:fim_byte]

    pacote = f"{i+1:05d}|".encode() + chunk

    while True:
        clientSocket.sendto(pacote, (serverName, serverPort))
        print(f"Pacote {i+1}/{num_pacotes} enviado ({len(chunk)} bytes)")

        clientSocket.settimeout(1.5)
        try:
            ack, _ = clientSocket.recvfrom(1024)
            ack = ack.decode()

            if ack.startswith("ACK"):
                print(" → OK:", ack)
                break

            elif ack.startswith("NACK"):
                print(" → ERRO DETECTADO (NACK), reenviando pacote...")

        except timeout:
            print(" → TIMEOUT (perda simulada), reenviando...")

# Finaliza transmissão
clientSocket.sendto(b"END", (serverName, serverPort))
print("\nArquivo enviado com sucesso!")

fim = time.time()
tempo_total = fim - inicio

print("\n=== Estatísticas ===")
print(f"Arquivo: {os.path.basename(arquivo_path)}")
print(f"Pacotes enviados: {num_pacotes}")
print(f"Tamanho de cada pacote: {tam_pacote} bytes")
print(f"Tamanho total: {tamanho_total} bytes")
print(f"Tempo total: {tempo_total:.2f} s")
print(f"Taxa média: {tamanho_total/tempo_total/1024:.2f} KB/s")

clientSocket.close()

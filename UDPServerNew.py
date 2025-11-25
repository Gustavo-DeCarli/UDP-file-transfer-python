from socket import *
import os
import random

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("", serverPort))

print("Servidor pronto para receber arquivos...")
print(f"Endereço de recepção: 0.0.0.0:{serverPort}\n")

# Probabilidades de perda e erro
prob_perda = 0.15   # 15% dos pacotes são ignorados
prob_erro  = 0.10   # 10% chegam "corrompidos"

arquivo = None
arquivo_nome = ""
pacotes_recebidos = 0
num_pacotes_esperados = 0

while True:
    message, clientAddress = serverSocket.recvfrom(4096)

    # Início da transferência
    if message.startswith(b"START|"):
        partes = message.decode().split("|")
        arquivo_nome = partes[1]
        tamanho_total = int(partes[2])
        num_pacotes_esperados = int(partes[3])

        arquivo = open(arquivo_nome, "wb")
        pacotes_recebidos = 0

        print(f"\nIniciando recebimento do arquivo '{arquivo_nome}' ({tamanho_total} bytes)")
        serverSocket.sendto(b"OK", clientAddress)
        continue

    # Fim da transferência
    if message == b"END":
        if arquivo:
            arquivo.close()
            print(f"\nTransferência concluída! Arquivo salvo como '{arquivo_nome}'")
            print(f"Pacotes recebidos: {pacotes_recebidos}/{num_pacotes_esperados}\n")
            arquivo = None
        continue

    # Processamento dos pacotes
    try:
        cabecalho, chunk = message.split(b"|", 1)
        num_pacote = int(cabecalho.decode())

        # --- SIMULA PERDA ---
        if random.random() < prob_perda:
            print(f"[PERDIDO] Pacote {num_pacote} descartado pelo servidor.")
            continue  # não envia ACK

        # --- SIMULA ERRO ---
        if random.random() < prob_erro:
            print(f"[ERRO] Pacote {num_pacote} corrompido. Enviando NACK...")
            serverSocket.sendto(f"NACK {num_pacote}".encode(), clientAddress)
            continue

        # Pacote OK
        pacotes_recebidos += 1
        arquivo.write(chunk)
        print(f"Pacote {num_pacote} recebido ({len(chunk)} bytes)")

        serverSocket.sendto(f"ACK {num_pacote}".encode(), clientAddress)

    except Exception as e:
        print("Erro ao processar pacote:", e)
        continue

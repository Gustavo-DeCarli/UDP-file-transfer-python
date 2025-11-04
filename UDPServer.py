from socket import *
import os

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("", serverPort))

# Obtém o IP local da máquina
# hostname = gethostname()
# local_ip = gethostbyname(hostname)

print("Servidor pronto para receber arquivos...")
print(f"Endereço de recepção: 192.168.100.119:{serverPort}\n")

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

        nome_destino = arquivo_nome
        arquivo = open(nome_destino, "wb")

        pacotes_recebidos = 0
        print(f"Iniciando recebimento do arquivo '{arquivo_nome}' ({tamanho_total} bytes)")
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

    # Recebimento de pacotes de dados
    try:
        cabecalho, chunk = message.split(b"|", 1)
        num_pacote = int(cabecalho.decode())
        pacotes_recebidos += 1

        arquivo.write(chunk)
        print(f"Pacote {num_pacote} recebido ({len(chunk)} bytes)")
        ack_msg = f"ACK {num_pacote}".encode()
        serverSocket.sendto(ack_msg, clientAddress)
    except Exception as e:
        print("Erro ao processar pacote:", e)
        continue

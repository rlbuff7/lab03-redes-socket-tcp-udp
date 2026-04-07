import socket

IP_servidor = "localhost"   # endereço onde o Server será executado
PORTA_servidor = 5005       # porta aberta pelo Server para conexão

# Criação de socket UDP
# AF_INET: família do protocolo IPv4
# SOCK_DGRAM: indica que será UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# IP e porta que o servidor deve aguardar a conexão
sock.bind((IP_servidor, PORTA_servidor))

while True:
    # Recebe mensagem via socket - aloca 1024 bytes
    # separa dados e endereço de origem
    data, addr = sock.recvfrom(1024)
    print("Mensagem recebida de:", addr)
    print("Mensagem recebida:", data)
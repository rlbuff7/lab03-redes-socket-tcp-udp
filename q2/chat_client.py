"""
Chat TCP - Cliente
Questão 2 - LAB03 Redes de Computadores
Porta: primeiros 5 dígitos do TIA
"""
import socket
import threading

IP_SERVIDOR = 'localhost'  # Altere para o IP do servidor se estiver em outra máquina
PORTA = 10427

encerrado = False

def receber_mensagens(sock):
    global encerrado
    while not encerrado:
        try:
            msg = sock.recv(1024).decode('utf-8')
            if not msg:
                break
            if msg.strip().upper() == 'QUIT':
                print("[Sistema] Servidor enviou QUIT. Encerrando...")
                encerrado = True
                break
            print(f"Servidor: {msg}")
        except:
            break

def main():
    global encerrado
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((IP_SERVIDOR, PORTA))
    print(f"[Sistema] Conectado ao servidor {IP_SERVIDOR}:{PORTA}")
    print("Digite mensagens (QUIT para encerrar):\n")

    t = threading.Thread(target=receber_mensagens, args=(cliente,), daemon=True)
    t.start()

    while not encerrado:
        try:
            msg = input()
        except EOFError:
            break
        if not encerrado:
            cliente.send(msg.encode('utf-8'))
        if msg.strip().upper() == 'QUIT':
            encerrado = True
            break

    cliente.close()
    print("[Sistema] Conexão encerrada.")

if __name__ == '__main__':
    main()

"""
Chat TCP - Servidor
Questão 2 - LAB03 Redes de Computadores
Porta: primeiros 5 dígitos do TIA
"""
import socket
import threading

PORTA = 10427

encerrado = False

def receber_mensagens(conn):
    global encerrado
    while not encerrado:
        try:
            msg = conn.recv(1024).decode('utf-8')
            if not msg:
                break
            if msg.strip().upper() == 'QUIT':
                print("[Sistema] Cliente enviou QUIT. Encerrando...")
                encerrado = True
                break
            print(f"Cliente: {msg}")
        except:
            break

def main():
    global encerrado
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(('', PORTA))
    servidor.listen(1)
    print(f"Servidor aguardando conexão na porta {PORTA}...")

    conn, addr = servidor.accept()
    print(f"[Sistema] Cliente conectado: {addr}")
    print("Digite mensagens (QUIT para encerrar):\n")

    t = threading.Thread(target=receber_mensagens, args=(conn,), daemon=True)
    t.start()

    while not encerrado:
        try:
            msg = input()
        except EOFError:
            break
        if not encerrado:
            conn.send(msg.encode('utf-8'))
        if msg.strip().upper() == 'QUIT':
            encerrado = True
            break

    conn.close()
    servidor.close()
    print("[Sistema] Conexão encerrada.")

if __name__ == '__main__':
    main()

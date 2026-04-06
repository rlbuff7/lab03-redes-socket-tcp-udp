"""
Servidor de Chat Multi-cliente com Transferência de Arquivos
Questão 3 - LAB03 Redes de Computadores

Funcionalidades:
  - Múltiplos clientes simultâneos via threads
  - Broadcast de mensagens entre todos os clientes conectados
  - Upload de arquivos para o servidor (cliente envia)
  - Download de arquivos do servidor (cliente solicita)
  - Listagem de arquivos disponíveis no servidor
  - Desconexão com comando QUIT

Comandos disponíveis para o cliente:
  /listar          - Lista arquivos disponíveis no servidor
  /enviar          - Envia um arquivo ao servidor
  /baixar <nome>   - Baixa um arquivo do servidor
  QUIT             - Encerra a conexão
  <texto>          - Envia mensagem para todos os outros clientes
"""
import socket
import threading
import os

HOST = ''
PORTA = 65432
PASTA = 'arquivos_servidor'
BUFFER = 4096

clientes = {}   # conn -> nome
lock = threading.Lock()

os.makedirs(PASTA, exist_ok=True)


def broadcast(mensagem: str, remetente=None):
    """Envia uma mensagem para todos os clientes exceto o remetente."""
    with lock:
        alvos = list(clientes.keys())
    for conn in alvos:
        if conn is remetente:
            continue
        try:
            conn.send(mensagem.encode('utf-8'))
        except Exception:
            pass


def listar_arquivos() -> str:
    arquivos = os.listdir(PASTA)
    if not arquivos:
        return "[Servidor] Nenhum arquivo disponível.\n"
    return "[Servidor] Arquivos disponíveis:\n" + "\n".join(f"  • {f}" for f in arquivos) + "\n"


def receber_arquivo(conn, cabecalho: str):
    """Protocolo: cliente envia 'UPLOAD:<nome>:<tamanho>' e depois os bytes."""
    try:
        _, nome_arquivo, tamanho_str = cabecalho.split(':', 2)
        tamanho = int(tamanho_str)
    except ValueError:
        conn.send("[Erro] Cabeçalho de upload inválido.\n".encode('utf-8'))
        return None

    conn.send("PRONTO\n".encode('utf-8'))  # sinaliza que pode enviar
    caminho = os.path.join(PASTA, os.path.basename(nome_arquivo))
    recebido = 0

    with open(caminho, 'wb') as f:
        while recebido < tamanho:
            chunk = conn.recv(min(BUFFER, tamanho - recebido))
            if not chunk:
                break
            f.write(chunk)
            recebido += len(chunk)

    return nome_arquivo if recebido == tamanho else None


def enviar_arquivo(conn, nome_arquivo: str):
    """Protocolo: servidor envia 'DOWNLOAD:<nome>:<tamanho>' e depois os bytes."""
    caminho = os.path.join(PASTA, os.path.basename(nome_arquivo))
    if not os.path.exists(caminho):
        conn.send(f"[Erro] Arquivo '{nome_arquivo}' não encontrado.\n".encode('utf-8'))
        return

    tamanho = os.path.getsize(caminho)
    conn.send(f"DOWNLOAD:{nome_arquivo}:{tamanho}\n".encode('utf-8'))

    # Aguarda ACK do cliente antes de enviar bytes
    ack = conn.recv(8).decode('utf-8').strip()
    if ack != 'ACK':
        return

    with open(caminho, 'rb') as f:
        while True:
            chunk = f.read(BUFFER)
            if not chunk:
                break
            conn.send(chunk)


def handle_client(conn, addr):
    """Thread dedicada a cada cliente conectado."""
    try:
        conn.send("[Servidor] Digite seu nome: ".encode('utf-8'))
        nome = conn.recv(256).decode('utf-8').strip() or str(addr)
    except Exception:
        conn.close()
        return

    with lock:
        clientes[conn] = nome

    print(f"[+] {nome} ({addr}) conectado. Total: {len(clientes)}")
    boas_vindas = (
        f"[Servidor] Bem-vindo, {nome}!\n"
        "Comandos: /listar | /enviar | /baixar <arquivo> | QUIT\n"
    )
    conn.send(boas_vindas.encode('utf-8'))
    broadcast(f"[Servidor] {nome} entrou no chat.\n", remetente=conn)

    try:
        while True:
            dados = conn.recv(BUFFER)
            if not dados:
                break

            msg = dados.decode('utf-8').strip()

            if msg.upper() == 'QUIT':
                conn.send("[Servidor] Até mais!\n".encode('utf-8'))
                break

            elif msg == '/listar':
                conn.send(listar_arquivos().encode('utf-8'))

            elif msg.startswith('UPLOAD:'):
                # Protocolo de upload iniciado pelo cliente
                nome_arq = receber_arquivo(conn, msg)
                if nome_arq:
                    print(f"[*] Arquivo '{nome_arq}' recebido de {nome}.")
                    conn.send(f"[Servidor] Arquivo '{nome_arq}' recebido com sucesso.\n".encode('utf-8'))
                    broadcast(
                        f"[Servidor] {nome} compartilhou '{nome_arq}'. Use /baixar {nome_arq}\n",
                        remetente=conn,
                    )
                else:
                    conn.send("[Erro] Falha no recebimento do arquivo.\n".encode('utf-8'))

            elif msg.startswith('/baixar '):
                nome_arq = msg[8:].strip()
                enviar_arquivo(conn, nome_arq)

            else:
                # Mensagem de chat — broadcast para todos
                linha = f"[{nome}]: {msg}\n"
                print(linha, end='')
                broadcast(linha, remetente=conn)

    except Exception as e:
        print(f"[!] Erro com {nome}: {e}")
    finally:
        with lock:
            clientes.pop(conn, None)
        broadcast(f"[Servidor] {nome} saiu do chat.\n", remetente=conn)
        print(f"[-] {nome} desconectado. Total: {len(clientes)}")
        conn.close()


def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORTA))
    servidor.listen(10)
    print(f"Servidor iniciado na porta {PORTA}. Aguardando conexões...")

    try:
        while True:
            conn, addr = servidor.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print("\n[Sistema] Servidor encerrado.")
    finally:
        servidor.close()


if __name__ == '__main__':
    main()

"""
Cliente de Chat com Transferência de Arquivos
Questão 3 - LAB03 Redes de Computadores

Comandos disponíveis:
  /listar          - Lista arquivos disponíveis no servidor
  /enviar          - Abre menu para escolher e enviar um arquivo
  /baixar <nome>   - Baixa um arquivo do servidor para a pasta local
  QUIT             - Encerra a conexão
  <texto>          - Envia mensagem para o chat
"""
import socket
import threading
import os

IP_SERVIDOR = 'localhost'  # Altere para o IP do servidor se necessário
PORTA = 65432
PASTA_DOWNLOADS = 'downloads'
BUFFER = 4096

encerrado = False

os.makedirs(PASTA_DOWNLOADS, exist_ok=True)


def receber_mensagens(sock):
    """Thread que fica escutando mensagens/dados vindos do servidor."""
    global encerrado
    buffer_acumulado = b''

    while not encerrado:
        try:
            dados = sock.recv(BUFFER)
            if not dados:
                print("\n[Sistema] Servidor encerrou a conexão.")
                encerrado = True
                break

            buffer_acumulado += dados

            # Verifica se é início de download de arquivo
            texto = buffer_acumulado.decode('utf-8', errors='replace')
            if texto.startswith('DOWNLOAD:'):
                linha, _, resto = texto.partition('\n')
                _, nome_arq, tamanho_str = linha.split(':', 2)
                tamanho = int(tamanho_str)

                # Envia ACK para o servidor começar a transmitir
                sock.send("ACK\n".encode('utf-8'))

                # Recebe os bytes do arquivo
                caminho = os.path.join(PASTA_DOWNLOADS, os.path.basename(nome_arq))
                bytes_arq = resto.encode('utf-8', errors='replace')  # bytes já recebidos
                recebido = len(bytes_arq)

                with open(caminho, 'wb') as f:
                    f.write(bytes_arq)
                    while recebido < tamanho:
                        chunk = sock.recv(min(BUFFER, tamanho - recebido))
                        if not chunk:
                            break
                        f.write(chunk)
                        recebido += len(chunk)

                print(f"\n[Sistema] Arquivo '{nome_arq}' salvo em '{PASTA_DOWNLOADS}/'.")
                buffer_acumulado = b''

            elif texto == 'PRONTO\n':
                # O servidor confirmou que está pronto para receber upload
                # Sinal tratado na thread principal — apenas limpa o buffer
                buffer_acumulado = b''

            else:
                # Texto normal — imprime completo somente se tiver newline
                while '\n' in texto:
                    linha, _, texto = texto.partition('\n')
                    print(f"\r{linha}")
                buffer_acumulado = texto.encode('utf-8')

        except Exception:
            if not encerrado:
                print("\n[Sistema] Conexão perdida.")
                encerrado = True
            break


def escolher_arquivo() -> tuple[str, int] | None:
    """Exibe os arquivos do diretório atual e pede ao usuário que escolha um."""
    arquivos = [f for f in os.listdir('.') if os.path.isfile(f)]
    if not arquivos:
        print("[Sistema] Nenhum arquivo encontrado no diretório atual.")
        return None

    print("\nEscolha um arquivo para enviar:")
    for i, f in enumerate(arquivos, 1):
        tamanho = os.path.getsize(f)
        print(f"  [{i}] {f}  ({tamanho} bytes)")

    escolha = input("Número do arquivo (ou ENTER para cancelar): ").strip()
    if not escolha:
        return None

    try:
        idx = int(escolha) - 1
        if 0 <= idx < len(arquivos):
            nome = arquivos[idx]
            return nome, os.path.getsize(nome)
    except ValueError:
        pass

    print("[Sistema] Escolha inválida.")
    return None


def enviar_arquivo(sock, nome: str, tamanho: int):
    """Protocolo de upload: envia cabeçalho, espera PRONTO, depois envia bytes."""
    cabecalho = f"UPLOAD:{nome}:{tamanho}\n"
    sock.send(cabecalho.encode('utf-8'))

    # Aguarda confirmação do servidor (PRONTO)
    resposta = b''
    while b'PRONTO' not in resposta:
        resposta += sock.recv(32)

    with open(nome, 'rb') as f:
        while True:
            chunk = f.read(BUFFER)
            if not chunk:
                break
            sock.send(chunk)

    print(f"[Sistema] Arquivo '{nome}' enviado com sucesso.")


def main():
    global encerrado

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP_SERVIDOR, PORTA))

    # Recebe prompt de nome e envia
    prompt = sock.recv(256).decode('utf-8')
    nome = input(prompt).strip()
    sock.send(nome.encode('utf-8'))

    # Inicia thread de recebimento
    t = threading.Thread(target=receber_mensagens, args=(sock,), daemon=True)
    t.start()

    print("\nConectado! Digite mensagens ou use os comandos disponíveis.\n")

    while not encerrado:
        try:
            cmd = input()
        except (EOFError, KeyboardInterrupt):
            cmd = 'QUIT'

        if encerrado:
            break

        if cmd.strip().upper() == 'QUIT':
            sock.send('QUIT'.encode('utf-8'))
            encerrado = True
            break

        elif cmd.strip() == '/enviar':
            resultado = escolher_arquivo()
            if resultado:
                nome_arq, tamanho = resultado
                enviar_arquivo(sock, nome_arq, tamanho)

        else:
            sock.send(cmd.encode('utf-8'))

    sock.close()
    print("[Sistema] Desconectado.")


if __name__ == '__main__':
    main()

# LAB03 – Sockets TCP e UDP | Redes de Computadores

**Alunos:**
- Rodrigo Lucas — TIA: 10427925
- Cristian Souza — TIA: 10436050

**Disciplina:** Redes de Computadores — Universidade Presbiteriana Mackenzie

---

## O que é este projeto?

Este laboratório implementa comunicação em rede usando **sockets TCP e UDP** em Python. Foram desenvolvidas três questões:

| Questão | O que faz |
|---------|-----------|
| Q1 | Análise teórica das diferenças entre TCP e UDP |
| Q2 | Chat bidirecional simples entre dois computadores (TCP) |
| Q3 | Chat em grupo com múltiplos usuários + envio e recebimento de arquivos (TCP) |

---

## Pré-requisitos

Antes de rodar qualquer coisa, você precisa ter instalado:

- **Python 3.10 ou superior** → [Download em python.org](https://www.python.org/downloads/)
- Nenhuma biblioteca extra é necessária — tudo usa módulos já incluídos no Python

Para verificar se o Python está instalado, abra o terminal e digite:
```bash
python --version
```

---

## Estrutura de arquivos

```
LAB03/
├── README.md                 ← este arquivo
├── respostas_q1.md           ← respostas teóricas da Questão 1
├── q2/
│   ├── chat_server.py        ← servidor do chat (Q2)
│   └── chat_client.py        ← cliente do chat (Q2)
└── q3/
    ├── server.py             ← servidor multi-cliente (Q3)
    ├── client.py             ← cliente com menu interativo (Q3)
    └── arquivos_servidor/    ← pasta criada automaticamente para arquivos compartilhados
```

---

## Questão 1 – Análise TCP e UDP

Respostas teóricas disponíveis em [respostas_q1.md](respostas_q1.md).

---

## Questão 2 – Chat TCP Bidirecional

Chat simples entre **dois computadores** via TCP. Qualquer lado pode enviar mensagens livremente. Digitar `QUIT` encerra a sessão.

### Como rodar (passo a passo)

> Você vai precisar de **dois terminais abertos** — um para o servidor, outro para o cliente.

**Terminal 1 — Servidor (inicie este primeiro):**
```bash
cd q2
python chat_server.py
```
Você verá: `Aguardando conexão na porta 10427...`

**Terminal 2 — Cliente (após o servidor estar rodando):**
```bash
cd q2
python chat_client.py
```
Você verá: `Conectado ao servidor!`

Agora é só digitar mensagens em qualquer terminal — elas aparecem no outro lado.

### Rodando em máquinas diferentes?

Se o cliente e o servidor estiverem em computadores diferentes na mesma rede:

1. Descubra o IP da máquina do servidor (no Windows: `ipconfig` no terminal)
2. Abra o arquivo `q2/chat_client.py`
3. Troque `IP_SERVIDOR = "127.0.0.1"` pelo IP real, por exemplo: `IP_SERVIDOR = "192.168.1.10"`

---

## Questão 3 – Chat Multi-cliente com Transferência de Arquivos

Versão avançada que suporta **vários usuários ao mesmo tempo** e permite **enviar e receber arquivos** pelo chat.

**Funcionalidades:**
- Vários clientes conectados simultaneamente
- Mensagens enviadas para todos no chat (broadcast)
- Upload de arquivos para o servidor
- Download de arquivos do servidor (salvos na pasta `downloads/`)
- Listagem dos arquivos disponíveis

### Comandos disponíveis no cliente

| Comando | O que faz |
|---------|-----------|
| `/listar` | Mostra os arquivos disponíveis no servidor |
| `/enviar` | Abre um menu para escolher e enviar um arquivo |
| `/baixar nome_do_arquivo.txt` | Baixa o arquivo indicado para a pasta `downloads/` |
| `QUIT` | Encerra sua conexão |
| qualquer outro texto | Envia mensagem para todos no chat |

### Como rodar (passo a passo)

> Você vai precisar de **pelo menos dois terminais** — um para o servidor e um ou mais para os clientes.

**Terminal 1 — Servidor (inicie este primeiro):**
```bash
cd q3
python server.py
```
Você verá: `Servidor iniciado. Aguardando conexões...`

**Terminal 2, 3, ... — Clientes (um terminal por usuário):**
```bash
cd q3
python client.py
```
O cliente pedirá um apelido (nickname) e então entrará no chat.

### Rodando em máquinas diferentes?

Mesma lógica da Q2:

1. Descubra o IP da máquina do servidor com `ipconfig`
2. Abra `q3/client.py`
3. Troque `IP_SERVIDOR = "127.0.0.1"` pelo IP real

---

## Vídeos de demonstração

main -> links
- **Vídeo 1 (Q1 + Q2):** _link do YouTube_
- **Vídeo 2 (Q3):** _link do YouTube_

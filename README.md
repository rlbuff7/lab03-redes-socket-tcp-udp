# LAB03 – Socket UDP e TCP | Redes de Computadores

**Aluno:** Rodrigo Lucas | TIA: 10427925  
**Disciplina:** Redes de Computadores – Universidade Presbiteriana Mackenzie

---

## Estrutura do repositório

```
LAB03/
├── respostas_q1.md          # Respostas teóricas da Questão 1
├── q2/
│   ├── chat_server.py       # Servidor TCP do chat bidirecional (Q2)
│   └── chat_client.py       # Cliente TCP do chat bidirecional (Q2)
└── q3/
    ├── server.py            # Servidor multi-cliente com threads e transferência de arquivos (Q3)
    ├── client.py            # Cliente com menu interativo (Q3)
    └── arquivos_servidor/   # Pasta criada automaticamente para armazenar arquivos compartilhados
```

---

## Questão 1 – Análise TCP e UDP

Veja as respostas detalhadas em [respostas_q1.md](respostas_q1.md).

---

## Questão 2 – Chat TCP Bidirecional

Chat simples entre cliente e servidor via TCP. Qualquer lado pode enviar mensagens livremente. O envio de `QUIT` por qualquer parte encerra a sessão.

**Porta usada:** `10427` (primeiros 5 dígitos do TIA)

### Como executar

1. **Inicie o servidor primeiro:**
   ```bash
   cd q2
   python chat_server.py
   ```

2. **Em outro terminal, inicie o cliente:**
   ```bash
   cd q2
   python chat_client.py
   ```

> Se o cliente e o servidor estiverem em máquinas diferentes, edite `IP_SERVIDOR` em `chat_client.py` com o IP da máquina do servidor.

---

## Questão 3 – Chat Multi-cliente com Transferência de Arquivos

Aplicação mais completa que demonstra o uso avançado de sockets TCP:

- **Múltiplas conexões simultâneas** gerenciadas por threads (uma thread por cliente)
- **Chat em grupo:** mensagens broadcast para todos os participantes conectados
- **Upload de arquivos** ao servidor com seleção interativa via menu
- **Download de arquivos** do servidor para pasta local `downloads/`
- **Listagem** dos arquivos disponíveis no servidor

### Comandos disponíveis no cliente

| Comando | Descrição |
|---|---|
| `/listar` | Lista arquivos disponíveis no servidor |
| `/enviar` | Exibe menu para escolher e enviar um arquivo |
| `/baixar <nome>` | Baixa o arquivo indicado para a pasta `downloads/` |
| `QUIT` | Encerra a conexão |
| `<qualquer texto>` | Envia mensagem para o chat (broadcast) |

### Como executar

1. **Inicie o servidor:**
   ```bash
   cd q3
   python server.py
   ```

2. **Em terminais separados, inicie quantos clientes quiser:**
   ```bash
   cd q3
   python client.py
   ```

> Para conectar de outra máquina, edite `IP_SERVIDOR` em `client.py`.

### Requisitos

- Python 3.10+
- Nenhuma biblioteca externa necessária (apenas módulos padrão: `socket`, `threading`, `os`)

---

## Vídeos de demonstração

- **Vídeo 1 (Q1 + Q2):** _link do YouTube_
- **Vídeo 2 (Q3):** _link do YouTube_

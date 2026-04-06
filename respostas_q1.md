# Questão 1 – Análise dos Sockets TCP e UDP

## a) Executar o cliente TCP antes do servidor TCP

**O que acontece:** O cliente TCP lança uma exceção de conexão recusada (`ConnectionRefusedError`) e encerra imediatamente.

**Por quê:** O TCP é um protocolo orientado a conexão. Antes de trocar qualquer dado, o cliente precisa concluir o *three-way handshake* (SYN → SYN-ACK → ACK) com o servidor. Como o servidor ainda não está escutando na porta, o sistema operacional retorna um pacote RST (reset), e o cliente interpreta isso como conexão recusada. Não existe canal estabelecido, portanto nenhum dado é transmitido.

---

## b) Executar o cliente UDP antes do servidor UDP

**O que acontece:** O cliente UDP envia o datagrama normalmente e **não** lança nenhuma exceção imediata. Porém, se ficar aguardando resposta (`recvfrom`), ficará bloqueado indefinidamente ou até o timeout, já que ninguém responde.

**Comparação com TCP:** O comportamento é diferente. No UDP não há estabelecimento de conexão — o cliente simplesmente dispara o datagrama. Se o servidor não estiver no ar, o pacote é descartado silenciosamente (a camada de transporte não avisa o remetente). Isso ilustra a principal diferença entre os dois protocolos:

| Característica | TCP | UDP |
|---|---|---|
| Orientado a conexão | Sim | Não |
| Confiabilidade | Garantida | Não garantida |
| Erro visível sem servidor | Imediato (`ConnectionRefusedError`) | Silencioso (pacote descartado) |
| Desempenho | Menor (overhead do handshake) | Maior (sem handshake) |

---

## c) Porta do cliente diferente da porta do servidor

**TCP:** O `connect()` falha com `ConnectionRefusedError`, pois nenhum serviço está escutando na porta indicada. O sistema operacional recebe um RST imediatamente.

**UDP:** O datagrama é enviado para a porta errada. O servidor nunca o recebe (está escutando em outra porta). Se o sistema operacional do servidor estiver ativo mas nenhum processo naquela porta, ele pode devolver um pacote ICMP *Port Unreachable*; dependendo da implementação, isso pode gerar `ConnectionResetError` no cliente ou simplesmente silêncio.

Em ambos os casos a comunicação falha, mas o TCP falha de forma explícita e imediata enquanto o UDP falha de forma silenciosa.

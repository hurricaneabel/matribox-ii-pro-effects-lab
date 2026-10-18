# Looper com retorno SysEx — V4

Teste físico confirmado pelo proprietário em 17/10/2026. O firmware acrescenta notificações do estado real do looper e dos controles Auto Rec, Drum Sync, Rec Level, PRE/POST e Play Volume. Acrescenta também o estado da camada de undo/redo. Mantém a biblioteca de 189 registros, os microfones nos cabinets e User IR e a remoção do Mic Lab separado.

O log do ensaio tem 57 mensagens, todas marcadas como mudanças, com cinco transições UNDO e cinco REDO. Foram observados vazio, gravação, reprodução, overdub e parado. O usuário confirmou funcionamento no aparelho. [Evidência resumida](../evidence/looper-v4-hardware-result.json); o log privado completo não é distribuído.

## Instalar e testar

Baixe a prerelease V4 na [aba Releases](https://github.com/hurricaneabel/matribox-ii-pro-effects-lab/releases). É um firmware experimental completo para **Matribox II Pro**, baseado no oficial V1.2.2; não é para Matribox II nem outros modelos. Foi testado em uma unidade, usando o atualizador oficial 1.2.0 em Windows 10 numa VM com USB atribuído ao convidado. Posteriormente, a atualização completa também foi confirmada diretamente no Windows 11 após configurar o driver nos dois modos; veja o [guia Windows 11](windows11-update.md).

Preserve um backup de presets, os arquivos IR/NAM e o firmware original para recuperação. Com a pedaleira em modo firmware, selecione o BIN no atualizador oficial e deixe concluir. Para retornar, use o firmware original completo pelo atualizador oficial. A preservação de dados em outras unidades não está garantida. O pacote não inclui um gravador próprio.

Após atualizar, deixe em modo normal, feche editor/frontend e use o monitor novo. Python 3.11 com `mido==1.3.3` e `python-rtmidi==1.5.8` foi usado no ensaio:

```sh
python monitor_looper_sysex.py --self-test
python monitor_looper_sysex.py
```

O monitor abre a entrada e envia uma única consulta de leitura, depois escuta. `--list` lista portas; `--input` e `--output` escolhem nomes exatos; `--no-query` desativa a consulta inicial. Se o Windows recusar abrir a porta, feche outros programas MIDI e reconecte o USB ao sistema escolhido (Windows 11 principal ou VM) antes de tentar novamente. Não é necessário regravar firmware por esse erro de abertura.

Grave uma base, faça overdub, termine o overdub e acione undo/redo. O monitor identifica as transições e grava JSONL. Não há envio periódico. Durante overdub, mudanças do índice nativo de histórico podem gerar mensagens legítimas mesmo sem mexer em controles.

## Protocolo experimental

Consulta exata: `F0 7D 4D 42 4C 51 01 F7` (identificador não comercial). Apenas solicita novo resumo; não modifica áudio ou configurações.

Resposta usa o envelope nativo, marcador `MBLP`, versão 3 e 16 bytes de payload, codificados em pares de nibbles. O frame completo tem 46 bytes. O monitor valida estrutura, sem usar o campo opaco do cabeçalho como checksum independente.

| Bytes do payload | Significado |
|---|---|
| 0–3 | ASCII MBLP |
| 4 | Versão 3 |
| 5 | Estado: 0 vazio, 1 parado, 2 não confirmado, 3 reprodução, 4 gravação, 5 overdub |
| 6 / 7 | Play Volume / Rec Level, 0–100 |
| 8 | 0 PRE, 1 POST |
| 9 | Flag nativa opaca, sem interpretação de interface |
| 10 / 11 | Drum Sync / Auto Rec |
| 12 | Histórico: 0 indisponível, 1 camada desfeita, 2 camada ativa |
| 13 | Índice nativo do histórico; 255 nenhum |
| 14–15 | Reservados, zero |

Undo/redo no monitor é inferido de transições 2→1 / 1→2 da mesma camada, fora de vazio/gravação/overdub. O resumo inicial não é uma ação. Após limpar, o firmware pode reter a flag antiga de histórico: a interface deve considerar VAZIO indisponível. Não é um contador de apertos; transições rápidas podem ser agrupadas ou perdidas em desconexão/fila cheia. Integração ao frontend ainda pendente.

## Validação e distribuição

Emulação verificou rotina original de undo/redo, operações ignoradas, 208 casos de configurações, consulta inicial e delegação de mensagens não correspondentes, fila cheia/repetição, 200 ciclos silenciosos e 934 textos de parâmetros idênticos. Biblioteca e blocos de recursos são idênticos à candidata de microfones já testada. Checksum do contêiner passou na rotina do atualizador original; isso não equivale a leitura independente da flash ou prova de todas as condições de áudio.

Firmware V4: SHA-256 `00d1f50553be869af12fdf8d28533b13d477d126722f589f0e581c7e20060b41`, 6.471.852 bytes. A release é experimental, não oficial, sem afiliação dos fabricantes. A licença MIT do repositório cobre apenas código e documentação originais do projeto; não relicencia firmware, algoritmos ou recursos de terceiros presentes no BIN.

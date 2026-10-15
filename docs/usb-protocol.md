# Protocolo observado no modo firmware

Descrição das capturas de pesquisa; não é uma especificação oficial. Um eco do seletor sozinho não comprova aceitação da transferência ou ausência de apagamento. A ferramenta pública desta versão lê capturas e não envia comandos.

| Mensagem | Papel observado |
|---|---|
| F0 7E 48 01 F7 | Consulta de identificação |
| F0 7E 48 7F 10 F7 | Seleção da biblioteca |
| F0 7E 48 02 … F7 | Anúncio de tamanho e quantidade |
| F0 7E 48 04 … F7 | Parcela de dados |
| F0 7E 48 03 7F F7 | Confirmação positiva |
| F0 7E 48 03 7E F7 | Resposta tratada como recusa pelo emissor |
| F0 7E 48 05 7B F7 | Término do bloco |
| F0 7E 48 07 F7 | Consulta de estado final |
| F0 7E 48 09 F7 | Conclusão |

O aviso de versão observado é `F0 7E 48 0B 01 56 31 32 32 00 F7` (V122). Ele precede a consulta inicial e reaparece no fluxo do atualizador. A omissão no primeiro ensaio e a recusa recebida são observações; sua função interna completa não foi demonstrada.

O anúncio contém dois uint32 big-endian (bytes reais e quantidade de pacotes), codificados em nibbles altos primeiro. Uma mensagem de dados contém índice mod 128, 180 bytes reais codificados em 360 nibbles, soma dos 360 nibbles mod 256 em dois nibbles, e F7. Total: 368 bytes. Última parcela preenchida com FF; tamanho anunciado determina o conteúdo efetivo.

A sessão sem compactação confirmou 12.019 pacotes de dados, mais anúncio, término e conclusão. A resposta final decodificada `483463df3539810b` também ocorreu em sessões com conteúdos diferentes. Não é apresentada como prova de checksum integral. Seu significado continua aberto.

## Verificar uma captura local

```sh
python -m matribox_lab capture local/session.pcapng --expected-library artifacts/library.bin
```

O analisador aceita PCAPNG little-endian com USBPcap linktype 249, exige identificação QME-200 e sessão completa, e verifica o conteúdo contra a biblioteca fornecida. Não preenche pacotes ausentes com dados do firmware. A captura completa original teve lacunas; as três sessões de biblioteca posteriores usadas como evidência estão completas.

As capturas contêm o próprio conteúdo do firmware e podem conter dados pessoais ou outros dispositivos; publique resumos revisados, não capturas brutas em issues. Nenhuma captura bruta é incluída neste repositório.

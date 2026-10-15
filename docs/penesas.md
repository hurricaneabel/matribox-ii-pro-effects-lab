# Reproduzir o Penesas documentado

O port corresponde ao registro Penesas/FaunDrive da GP-200 V1.8.2 em 0x43ED8C. O caráter associado a Klon é a referência indicada pelo usuário e sua avaliação auditiva; não uma medição comparativa de hardware.

## Entradas locais exatas

Consulte os hashes em [reference-inputs.json](../evidence/reference-inputs.json). O construtor rejeita entradas de firmware diferentes das documentadas; offsets não são autodetectados para novas versões.

```sh
python -m pip install -e ".[reverse]"
python experiments/rebuild_penesas.py --gp-firmware "local/GP-200_USB_Firmware_V1.8.2.bin" --output artifacts/penesas
python experiments/build_penesas_library.py --matribox-firmware "local/QME-200_FW_USB_V1.2.2.bin" --record artifacts/penesas/penesas_registro_experimental.bin --output artifacts/library.bin
```

O primeiro script recupera referências e cria ELF e descritor; o segundo acrescenta o registro ao catálogo original, sem compactar ou substituir seus módulos. Ambos trabalham somente em arquivos. A saída **não é um firmware completo**. Esta versão do projeto não fornece programa de gravação.

O hash esperado da biblioteca resultante é `72bba28a4239737d63e6a75b6762580dc77c4890de7b0ace81949995a9f6e6ac`. Essa reprodução foi conferida localmente antes da publicação.

## O que foi reconstruído

- Corpo doador ligado em 0x39200, constantes em 0x3B334, estado recuperado em 0x20216800.
- Prefixo e metadados no formato observado da Matribox; relocações reconstruídas.
- ELF de 18.392 bytes, registro de 18.520 bytes, estado reservado conservadoramente em 4.096 bytes.
- Controles Gain, Tone, Volume: 0..100, passo 1; padrões 40/50/50.
- Novo grupo/índice: Drive (3), índice 24; ID 0x03000014.

A descoberta de 2.068 locais de instrução alcançáveis, sem desvios diretos externos encontrados, não prova ausência de todas as dependências indiretas possíveis. A reserva de estado é conservadora, não inferência completa de todos os caminhos.

## Emulação e teste físico

Leitor/carregador ARM original aceitou o ELF. O código reconstruído e o corpo GP nos endereços de ligação produziram buffers e estado idênticos em quatro cenários: 80 blocos, 5.120 frames. Modelo explícito Cortex-M7 no Unicorn 2.1.4, modo Thumb sem a opção legada MCLASS. Não foi emulado o firmware inteiro.

Uma configuração anterior misturava MCLASS legado com seleção explícita de CPU e rejeitava conversões f32/f64, inclusive em um módulo nativo. A configuração corrigida resolveu essa divergência sem alterar o ELF. Não confundir esse diagnóstico histórico do emulador com incompatibilidade demonstrada no processador físico.

O proprietário confirmou áudio, controles e bypass. Salvou 50/100/100 e confirmou persistência após reiniciar. Na sessão posterior sem compactação, confirmou novamente funcionamento dos efeitos testados e preset retido. Esses relatos não substituem teste de todas as combinações ou medição de CPU/latência.

Os cenários sintéticos incluíram picos também presentes no código doador; não houve normalização adicionada pelo port. Uma eventual nova validação física deve considerar ganho da cadeia e começar com nível de escuta baixo.

## Evolução

A primeira candidata compactava metadados de 12 módulos para manter o tamanho original. A candidata de referência atual não compacta nenhum módulo original e cresce 18.524 bytes. O sucesso dessa extensão não determina o tamanho máximo permitido da biblioteca. Um novo efeito exige análise própria de código, dependências, parâmetros, memória e execução; similaridade de descrição em manual não basta.

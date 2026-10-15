# FRMW e catálogo de efeitos

Escopo: arquivos de referência V1.1.4 e V1.2.2 identificados por SHA-256. Não aplicar automaticamente a outras pedaleiras ou versões.

## Blocos do arquivo

Assinatura `FRMW`. Quatro pares little-endian `(offset_relativo, tamanho)` estão nos offsets `0x30`, `0x38`, `0x40` e `0x48`. O início absoluto é **offset_relativo + 0x30**.

| Posição no arquivo | Papel observado | Seletor no USB |
|---|---|---|
| 0 | Principal, incluindo código e outros recursos | 00 |
| 1 | Biblioteca de efeitos | 10 |
| 2 | Bloco de dados | 01 |
| 3 | Bloco de dados | 02 |

A ordem de envio da atualização completa observada é 00, 01, 02, 10. Os offsets no arquivo não são os destinos físicos de flash.

## Catálogo

| Offset da raiz | Campo |
|---|---|
| +04 | Tamanho do cabeçalho: 0x18 + 4 × grupos |
| +08 | Tamanho do cabeçalho e tabelas |
| +0C | Tamanho total da biblioteca |
| +14 | Número de grupos (16 nas referências) |
| +18 | Offsets de cada grupo, relativos à raiz |

Cada grupo contém `uint32 count`, seguido de `count` offsets de registros relativos à raiz. Um registro começa com tamanho total e offset interno do ELF, ambos uint32. O descritor em +8 começa pelo identificador do efeito. Contagem de parâmetros fica em +16; offsets de nome/categoria em +20/+22. Tabela de parâmetros começa em +24, 24 bytes por parâmetro, seguida de strings e alinhamento. O parser público verifica limites antes de acessar os dados.

ID, grupo e índice são conceitos distintos. Não inferir o grupo pelo byte alto do ID. Há ainda casos oficiais em que o ID do descritor difere do prefixo carregado do ELF (Pitch S).

## ELF

Módulos ARM32 little-endian com seções como ER_IROM, ER_SROM, ER_IRAM, ocasional ER_SRAM, símbolos e relocações. O carregador estudado copia e reloca o código antes de chamar Init/Process. O offset do arquivo principal usado para desmontagem foi endereço ARM +0x78; essa relação não vale para todo o FRMW ou para os ELF.

Rotinas V1.2.2: catálogo 0x1B180; preparação do ELF 0x1B538; leitor 0x4029C; carregador 0x405C8; inicializador de pools 0x409C0. São endereços obtidos por análise, não símbolos oficiais.

A candidata sem compactação reutiliza todos os registros V1.2.2, acrescenta o Penesas e reconstrói tabelas e tamanho. Resultado: 2.163.372 bytes, contra 2.144.848 originais. O script não produz invólucro FRMW nem transmite ao dispositivo.

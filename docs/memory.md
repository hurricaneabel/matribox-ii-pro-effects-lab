# Memória: dados conhecidos e perguntas abertas

## Flash configurada: 8 MiB

Tabela FlexSPI V1.2.2 em 0x47290: campo +8 = 0x2000. A inicialização copia a tabela e passa o campo ao controlador; a documentação [NXP FlexSPI](https://mcuxpresso.nxp.com/api_doc/dev/1581/group__flexspi.html) define flashSize em KByte. Isso corresponde a 8.192 KiB, ou 8 MiB configurados. O ID JEDEC físico não foi lido.

O chip de SDRAM fotografado é W9825G6KH-6; a família Winbond é de 256 Mbit (32 MiB). Essa RAM não é o espaço persistente do catálogo. Os pools efetivamente usados pelo carregador são outra restrição:

| Pool configurado | Bytes |
|---|---:|
| Código | 131.072 |
| Estado IRAM | 196.608 |
| Constantes | 131.072 |
| Estado SRAM externo | 7.139.328 |

Esses valores vieram da execução emulada do inicializador original; não medem memória livre no firmware inteiro em operação. Fonte da capacidade SDRAM: [Winbond W9825G6KH](https://www.winbond.com/hq/new-online-purchasing-guide/index.html?__locale=zh_CN&pLine=%2Fproduct%2Fcustomized-memory-solution%2Fddr-sdr%2F&pNo=W9825G6KH-6A), variante da mesma família.

## Biblioteca

A inicialização aponta para 0x60480000, offset 0x480000 na janela de flash 0x60000000. A V1.2.2 tem 2.144.848 bytes; a candidata sem compactação tem 2.163.372. Na correspondência contígua esperada, o fim passa de 0x68BA50 para 0x6902AC; arredondamento de setores de 0x68C000 para 0x691000, cinco setores adicionais de 4 KiB.

A sessão maior foi aceita e o funcionamento foi relatado, mas não houve dump independente da flash. Alcance real de apagamento e propriedade dos setores vizinhos continuam não estabelecidos. A existência de outra região em 0x700000 não prova que a lacuna anterior seja livre.

**Ainda não existe número seguro de quantos efeitos extras cabem.** Precisamos identificar a capacidade reservada à biblioteca e os limites da interface/presets. Somar espaço dos registros e quatro bytes por nova referência resolve apenas parte da conta; RAM e CPU limitam os efeitos simultâneos. Oito MiB totais menos o tamanho do arquivo de atualização não é uma medida de espaço livre.

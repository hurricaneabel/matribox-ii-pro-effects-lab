# Microfones integrados em cabinets e User IR

Atualização: 17/10/2026. Pesquisa e testes em uma unidade Matribox II Pro, com firmware-base V1.2.2. Esta é a referência experimental local mais recente; os binários continuam fora do repositório público.

## Resultado físico relatado

- Supero 1x6: integração inicial funcionou; os nomes dos microfones também foram confirmados na tela.
- Cabinets de fábrica: o proprietário testou 20 cabinets diferentes, alternando microfones e posições, e relatou funcionamento correto. O banco contém 61; os outros 41 não foram individualmente confirmados em hardware.
- User IR: após estender a camada aos IRs importados, o proprietário relatou funcionamento perfeito. Quantidade de IRs, reimportação, salvar e reiniciar não foram discriminados nessa confirmação final.
- Mic Lab/Mic Studio separado foi removido da MOD na candidata atual. Os demais índices permaneceram iguais.

## Controles e escopo

Volume, Low Cut e High Cut foram mantidos. Foram acrescentados Mic Type, Position X, Position Y e Position Z. Mic Type **Off** desativa a camada adicional. As posições vão de 0 a 100.

| Valor | Nome exibido |
|---|---|
| 0 | Off |
| 1 | Dyn57 |
| 2 | Dyn58 |
| 3 | Dyn421 |
| 4 | Dyn16 |
| 5 | Dyn112 |
| 6 | Dyn609 |
| 7 | ConU67 |
| 8 | Con87A |
| 9 | Con U87 |
| 10 | Rib 121 |

Os nomes foram rastreados na rotina de interface da Ampero Mini; não são identificações deduzidas apenas pelo timbre. Os eixos são apresentados como X/Y/Z, sem afirmar medidas físicas em centímetros. O processamento é o cabinet/IR original da Matribox seguido dos filtros de microfone e posição recuperados da Ampero Mini: não é uma importação integral do sistema de cabinets da Ampero.

O código de importação, o protocolo e os arquivos de IR não foram modificados. A candidata altera o processamento do módulo User IR após carregar a resposta. Um IR pode já conter a resposta de um microfone; aplicar a camada muda essa resposta adicionalmente.

## Implementação e testes offline

Os módulos originais de cabinet e User IR têm ELF idênticos. O adaptador preserva a convolução original e acrescenta os filtros ao mesmo callback. O registro compartilhado do grupo 5 atende os cabinets de fábrica; o grupo 6 atende User IR. A candidata atual contém **189 registros**: o Mic Lab independente deixou de existir.

A interface recebeu um formatador de nomes em rotinas reservadas sem uso nos parâmetros do catálogo estudado. Uma correção estreita no leitor de defaults converte apenas a sentinela bruta FFFFFFFF em zero, preservando defaults válidos de outros módulos. A versão atual mantém o bloco principal idêntico à versão dos 61 cabinets; somente o registro User IR mudou nessa última etapa. Os outros 188 registros da biblioteca permanecem byte a byte iguais à etapa anterior.

Validações locais:

- Seleção nativa e identificação dos IRs dos 61 cabinets; com Mic Type Off, áudio idêntico ao módulo original nos casos testados.
- Comparação do callback integrado com cabinet original seguido dos filtros doadores: tipos, posições, bypass, reinicialização e troca de cabinet; buffers idênticos, valores finitos e preservação de registradores/limites de memória nos ensaios.
- 176 casos de exibição nativa de nomes e limites do buffer; defaults dos 20 slots User IR.
- Salvar/ler/aplicar presets nas 12 posições internas, com armazenamento modelado em RAM.
- Catálogo, carregador e alocação de uma cadeia específica incluindo CAB e User IR.
- Contêiner FRMW e execução da rotina de checksum do atualizador oficial; controle negativo rejeitado.

A atualização física usou o programa oficial 1.2.0 em VM Windows 10. Nenhum desses testes determina o limite máximo da flash, garante todas as cadeias ou constitui medição de prazo de áudio no hardware. A confirmação física é relato do proprietário; não houve leitura independente da flash.

## Presets e distribuição

Presets que usavam o Mic Lab separado precisam ser ajustados: a transferência dos seus controles para o CAB não é automática. Presets comuns mantêm IDs/índices; os controles novos têm default Off. É necessário conservar os backups e as fontes dos IRs/NAM usados localmente.

Não publicamos firmware, ELF do fabricante, biblioteca modificada ou pacote pronto para gravação. Os hashes e resumos permitem identificar as candidatas locais, sem transformar a documentação em garantia de compatibilidade com outras versões/unidades.

A emissão de estado do looper por SysEx é uma próxima investigação, ainda sem implementação ou validação.

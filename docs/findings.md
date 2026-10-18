# Resultados e qualidade da evidência

Registro inicial: 15/10/2026. Plataforma física: uma Matribox II Pro do proprietário. O processador fotografado é MIMXRT1062; a serigrafia da placa menciona MIMXRT1052Core, portanto a serigrafia não foi tomada como identificação final do chip.

## Firmware oficial

V1.1.4 contém 173 registros; V1.2.2 contém 179. Foram acrescentados Gate 3, Harmony D, Pitch S, Eko D, Ice Delay e Haze. Todos os 173 registros anteriores são idênticos byte por byte. A biblioteca cresceu 71.676 bytes: 71.652 de novos registros e 24 de novas referências.

Uma reconstrução usando os registros antigos e as seis adições reproduziu exatamente o bloco oficial novo, hash `94743693aa9a663d7ca0df6448c55169f6fd1a948ae21c642620cee07362a25d`. O bloco principal também mudou; não atribuímos todas as suas mudanças à adição de efeitos. Os dois blocos posteriores permaneceram iguais.

Ring Mod e Tape Mod mudaram dos índices 4/5 para 6/7 no grupo 1, mantendo os IDs e bytes dos registros. Portanto, preservar IDs não é o mesmo que preservar posição na lista.

## Port do Penesas

O algoritmo doador tem nome interno FaunDrive. O registro reconstruído foi adicionado ao grupo Drive (3), índice interno 24, ID `0x03000014`, controles Gain/Tone/Volume. O catálogo passou a 180 entradas.

A primeira candidata manteve o tamanho original compactando metadados de 12 ELF. O carregador original emulado produziu dados em memória idênticos para esses módulos. O proprietário confirmou seleção, áudio, controles, bypass e preset 50/100/100 preservado após desligar/ligar. Também relatou drives e amplificadores testados normais.

Depois, uma candidata sem compactação preservou todos os 179 registros originais integralmente e acrescentou 18.524 bytes. Foram confirmados 12.019 pacotes, boot normal, preset mantido e funcionamento normal dos efeitos testados. Esta é a referência preferida para o port, mas seu sucesso não revela o limite máximo da partição.

## Separação das evidências

- **Binário:** conteúdo e hashes dos arquivos, estrutura do catálogo e preservação dos registros.
- **Emulação:** execução do leitor/carregador ARM original, acessores de parâmetros e comparação de áudio sintético do Penesas com o código doador.
- **USB:** reconstrução de todos os bytes das sessões completas, índices, somas de pacotes e confirmações.
- **Relato físico do proprietário:** presença na tela, controles, áudio, bypass, reinicialização e persistência do preset.

Hash do tráfego USB não é uma leitura independente da flash. Igualdade com o algoritmo doador em emulação não é comparação instrumental com uma GP-200 ou Klon físico. Não foi medido tempo real/CPU no firmware completo, nem todas as combinações de efeitos.

## Falha anterior

A primeira tentativa isolada sem aviso inicial de versão recebeu recusa no anúncio. A tentativa com aviso aceitou dois pacotes e recusou o terceiro; o fechamento MIDI apresentou também uma exceção posterior. Os bytes gerados coincidiam com a captura bem-sucedida e com o parcelador nativo. A recuperação pelo firmware original completo no editor oficial do Windows 10 foi relatada como bem-sucedida. O ensaio no Windows 10 da VM depois completou a sessão isolada. Ambiente, transporte, contexto e versão de Python variaram; a causa específica da falha não foi estabelecida.

Os resumos públicos estão em [evidence/](../evidence/). Capturas completas e dados privados permanecem locais.

## Atualização: microfones em cabinets e User IR — 17/10/2026

A referência local mais recente passou a integrar os filtros no CAB e User IR, com nomes e X/Y/Z, removendo o módulo separado. O proprietário confirmou 20 cabinets e depois os IRs importados. A candidata tem 189 registros; não se aplica a ela a afirmação histórica de que todos os 179 registros originais são intactos, pois os registros CAB e User IR foram modificados. Detalhes e limites em [cabinet-microphones.md](cabinet-microphones.md), com [resumo de evidência](../evidence/microphones-hardware-result.json).

## Looper SysEx V4 — 17/10/2026

O proprietário confirmou funcionamento físico de estados, controles e undo/redo. O log contém 57 mensagens com cinco UNDO e cinco REDO. Sem resumos periódicos; mudanças internas de histórico durante overdub também geram eventos. Veja [protocolo, instalação e limites](looper-sysex.md).

## Looper SysEx V4 — 17/10/2026

O proprietário confirmou funcionamento físico de estados, controles e undo/redo. O log contém 57 mensagens com cinco UNDO e cinco REDO. Sem resumos periódicos; mudanças internas de histórico durante overdub também geram eventos. Veja [protocolo, instalação e limites](looper-sysex.md).

## Windows 11: atualização completa confirmada — 17/10/2026

Após selecionar USB Audio Device (`usbaudio`) nos dispositivos dos modos normal (PID 0282) e firmware (PID 0283), a consulta do looper, a identificação do bootloader e uma atualização completa da V4 funcionaram no host Windows 11. A transferência foi confirmada pelo usuário; não houve análise de captura desta sessão. [Guia](windows11-update.md) e [resultado](../evidence/windows11-update-result.json).

# Plano de desenvolvimento

## Confirmado nesta pesquisa

- [x] Decodificar FRMW, grupos, registros e ELF.
- [x] Comparar V1.1.4 e V1.2.2; reproduzir exatamente o empacotamento da biblioteca oficial nova.
- [x] Confirmar sessão exclusiva da biblioteca em uma unidade.
- [x] Reconstruir e testar Penesas, inclusive controles, bypass e persistência de preset.
- [x] Confirmar transferência da candidata sem compactação, com 179 registros originais idênticos.
- [x] Publicar ferramentas offline reproduzíveis e hashes de evidência.

## Atualização de 17/10/2026

- [x] Integrar a camada de microfone/posição ao CAB, com nomes no Mic Type.
- [x] Ampliar aos 61 cabinets de fábrica; 20 confirmados fisicamente pelo proprietário.
- [x] Ampliar ao User IR, mantendo importação intacta; funcionamento físico relatado.
- [x] Remover Mic Lab separado da MOD, mantendo os outros índices.
- [ ] Ampliar confirmação física e documentar cenários específicos de persistência/importação em User IR.
- [x] Implementar e testar retorno SysEx do looper, cinco controles e undo/redo, sem heartbeat periódico.
- [x] Preparar prerelease experimental V4 com firmware completo e monitor.
- [ ] Integrar o protocolo ao frontend, considerando VAZIO e limites das transições.

## Próximas investigações

- [ ] Estabelecer limite reservado à biblioteca e política de apagamento do bootloader.
- [ ] Entender o estado final de oito bytes; não tratá-lo como checksum sem prova.
- [ ] Analisar limites de índices, contagens, presets e listas do editor/frontend.
- [ ] Ampliar testes de dependências, inicialização de estado e consumo dos pools.
- [ ] Definir uma lista de efeitos desejados ausentes na Matribox, com fontes e parâmetros claros.
- [ ] Criar ensaios de conversão independentes para cada candidato antes de qualquer instalação.
- [ ] Consolidar ferramenta de empacotamento/validação; avaliar posteriormente um gerenciador.
- [ ] Rever separadamente a publicação de um executor físico com suporte a logs, interrupções e recuperação.

B-Chorus, B-Boost, C-Wah e Green OD serviram como controles de reconstrução na fase de emulação. Isso não transforma automaticamente qualquer módulo de outra pedaleira em compatível. Os resultados físicos posteriores estão descritos em [microfones e User IR](docs/cabinet-microphones.md); os controles de reconstrução não estabelecem compatibilidade universal.

Não usar preenchimento progressivo da flash como substituto para identificar as regiões. Novas versões/hardware precisam ser tratadas como alvos diferentes até haver evidência.

## Atualização direta no Windows 11 — 17/10/2026

- [x] Confirmar atualização completa da Lab V4 após trocar o driver MIDI nos modos normal e firmware; [procedimento](docs/windows11-update.md).

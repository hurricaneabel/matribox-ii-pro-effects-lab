# Plano de desenvolvimento

## Confirmado nesta pesquisa

- [x] Decodificar FRMW, grupos, registros e ELF.
- [x] Comparar V1.1.4 e V1.2.2; reproduzir exatamente o empacotamento da biblioteca oficial nova.
- [x] Confirmar sessão exclusiva da biblioteca em uma unidade.
- [x] Reconstruir e testar Penesas, inclusive controles, bypass e persistência de preset.
- [x] Confirmar transferência da candidata sem compactação, com 179 registros originais idênticos.
- [x] Publicar ferramentas offline reproduzíveis e hashes de evidência.

## Próximas investigações

- [ ] Estabelecer limite reservado à biblioteca e política de apagamento do bootloader.
- [ ] Entender o estado final de oito bytes; não tratá-lo como checksum sem prova.
- [ ] Analisar limites de índices, contagens, presets e listas do editor/frontend.
- [ ] Ampliar testes de dependências, inicialização de estado e consumo dos pools.
- [ ] Definir uma lista de efeitos desejados ausentes na Matribox, com fontes e parâmetros claros.
- [ ] Criar ensaios de conversão independentes para cada candidato antes de qualquer instalação.
- [ ] Consolidar ferramenta de empacotamento/validação; avaliar posteriormente um gerenciador.
- [ ] Rever separadamente a publicação de um executor físico com suporte a logs, interrupções e recuperação.

B-Chorus, B-Boost, C-Wah e Green OD serviram como controles de reconstrução na fase de emulação. Isso não transforma automaticamente qualquer módulo de outra pedaleira em compatível. Nenhum outro port físico é prometido nesta versão.

Não usar preenchimento progressivo da flash como substituto para identificar as regiões. Novas versões/hardware precisam ser tratadas como alvos diferentes até haver evidência.

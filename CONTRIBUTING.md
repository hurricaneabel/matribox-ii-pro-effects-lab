# Como contribuir

Abra uma issue com modelo/revisão do aparelho, versão e SHA-256 do firmware, objetivo do ensaio e quais evidências existem. Diferencie hipótese, teste offline, captura e teste físico. Não inclua tokens, presets pessoais, capturas completas ou firmware em issues/PRs.

Sugestões de efeitos devem trazer nome do efeito, pedaleira/versão doadora, controles e por que ele está ausente no catálogo alvo. Uma descrição semelhante no manual é pista, não prova de compatibilidade binária.

Para código, mantenha as ferramentas offline por padrão, entradas locais explícitas, verificações de tamanho/hash e testes que não dependam de firmwares distribuídos. Os testes sintéticos do repositório usam somente estruturas inventadas. Não acrescente envio MIDI/USB automático ou uma gravação como etapa de CI.

```sh
python -m pip install -e .
python -m unittest discover -s tests -v
```

A licença do projeto cobre contribuições originais; não republicar binários de terceiros sob a licença deste laboratório.

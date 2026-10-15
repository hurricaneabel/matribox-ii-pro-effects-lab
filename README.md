# Matribox II Pro Effects Lab

Pesquisa independente sobre o catálogo de efeitos, firmware e protocolo USB da **SONICAKE Matribox II Pro**, incluindo um port experimental do **Penesas da Valeton GP-200**.

**Resultado confirmado em uma unidade:** o Penesas foi acrescentado como nova entrada, sem substituir efeitos existentes. Gain, Tone, Volume, bypass e persistência em preset foram testados pelo proprietário. Uma biblioteca sem compactação preserva integralmente os 179 registros originais e acrescenta o Penesas, totalizando 180 entradas. A captura USB dessa sessão foi verificada offline.

Isso é um resultado experimental específico, não uma confirmação de compatibilidade de todos os efeitos, modelos ou versões de firmware. O limite máximo da região de biblioteca ainda é desconhecido. Os 8 MiB de flash configurados no firmware não são uma medida de espaço livre.

## O que está publicado

- [Resultados e fontes de evidência](docs/findings.md).
- [Formato FRMW e catálogo](docs/firmware-format.md).
- [Protocolo USB observado](docs/usb-protocol.md).
- [Reconstrução e testes do Penesas](docs/penesas.md).
- [Memória e limites ainda abertos](docs/memory.md).
- Ferramentas offline para inspecionar, comparar, reconstruir a candidata documentada e verificar capturas.
- [Plano de desenvolvimento](ROADMAP.md) e [como contribuir](CONTRIBUTING.md).

Esta versão não inclui um gravador USB, atualizador pronto ou gerenciador de efeitos. A reconstrução gera um bloco de biblioteca, **não um firmware completo para abrir no editor oficial**.

## Começar

Python 3.10 ou superior. As ferramentas de inspeção usam somente a biblioteca padrão:

```sh
python -m pip install -e .
python -m matribox_lab inspect "local/matribox-v1.2.2.bin"
python -m matribox_lab compare "local/matribox-v1.1.4.bin" "local/matribox-v1.2.2.bin"
python -m unittest discover -s tests -v
```

Os arquivos em `local/` são fornecidos pelo próprio usuário. Firmwares, ELF extraídos, bibliotecas de efeitos geradas, presets e capturas completas não estão incluídos. Os [hashes de referência](evidence/reference-inputs.json) identificam as entradas estudadas.

Para reproduzir a candidata **offline**, consulte [docs/penesas.md](docs/penesas.md). Esse processo foi conferido localmente e reproduz o hash da biblioteca sem compactação testada na pedaleira.

## Estado do projeto

| Área | Estado |
|---|---|
| Catálogo V1.1.4 / V1.2.2 | Decodificado e comparado |
| Atualização exclusiva da biblioteca | Sessões verificadas em USB e boot normal relatado |
| Penesas | Testado no aparelho pelo proprietário |
| 179 registros originais na candidata sem compactação | Idênticos byte por byte |
| Capacidade máxima para novos efeitos | Em investigação |
| Outros ports e gerenciador público | Planejados; sem promessa de compatibilidade |

As sessões físicas bem-sucedidas documentadas usaram Windows 10 em VM com USB conectado ao convidado. Houve uma falha anterior no host Windows 11; sua causa não foi isolada. Não se conclui que todo Windows 11 seja incompatível.

## English overview

Independent SONICAKE Matribox II Pro firmware and effect-catalog research. An experimental Valeton GP-200 Penesas port was tested on one physical unit. Offline tools reproduce the documented library from user-supplied firmware inputs; no vendor firmware or ready-to-flash library is distributed. See the source, evidence hashes and limitations before attempting to generalize the result.

## Licença e autoria

Mantido por [hurricaneabel](https://github.com/hurricaneabel). Código e documentação originais deste projeto sob [MIT](LICENSE). A licença não concede direitos sobre os firmwares ou algoritmos de terceiros usados como entradas locais. Projeto independente, sem afiliação ou aprovação declarada dos fabricantes.

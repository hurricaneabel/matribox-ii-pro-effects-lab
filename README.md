# Matribox II Pro Effects Lab

Pesquisa independente sobre o catálogo de efeitos, firmware e protocolo USB da **SONICAKE Matribox II Pro**, incluindo um port experimental do **Penesas da Valeton GP-200**.

**Nova pre-release (20/10/2026):** [Lab 5 — firmware, efeitos e origens](docs/lab5-firmware.md): indicador DSP na tela, 29 modelos portados da GP-200 no total, nove cabinets nativos, Cab Match, subclasses, defaults de microfones e corretivo da navegacao lateral. A ultima correcao de navegacao ainda aguarda confirmacao fisica. Veja o escopo dos testes antes de instalar pela [aba Releases](https://github.com/hurricaneabel/matribox-ii-pro-effects-lab/releases).

Os registros abaixo datados de 17/10 documentam a Lab 4 e os experimentos anteriores.

**Novidade (17/10/2026):** [looper com retorno SysEx, incluindo undo/redo](docs/looper-sysex.md), testado fisicamente. Firmware completo e monitor na [aba Releases](https://github.com/hurricaneabel/matribox-ii-pro-effects-lab/releases), como versão experimental.

**Referência de efeitos (17/10/2026):** microfones integrados nos cabinets de fábrica e nos IRs importados, com nomes no Mic Type e controles X/Y/Z. O proprietário confirmou 20 dos 61 cabinets, alternando microfones e posições, e depois confirmou funcionamento nos User IR. A candidata local tem 189 registros e remove o módulo de microfone separado da MOD. Veja [resultados, implementação e limites](docs/cabinet-microphones.md).

O Penesas também foi testado com Gain, Tone, Volume, bypass e persistência em preset. Sua reconstrução offline sem compactação permanece publicada como experimento reproduzível separado, com 179 registros originais intactos e 180 entradas totais.

Isso é um resultado experimental específico, não uma confirmação de compatibilidade de todos os efeitos, modelos ou versões de firmware. O limite máximo da região de biblioteca ainda é desconhecido. Os 8 MiB de flash configurados no firmware não são uma medida de espaço livre.

## O que está publicado

- [Atualização no Windows 11: driver nos dois modos](docs/windows11-update.md).
- [Looper SysEx e instalação da V4](docs/looper-sysex.md).
- [Atualização no Windows 11: driver nos dois modos](docs/windows11-update.md).
- [Looper SysEx e instalação da V4](docs/looper-sysex.md).
- [Microfones nos cabinets e User IR](docs/cabinet-microphones.md).
- [Resultados e fontes de evidência](docs/findings.md).
- [Formato FRMW e catálogo](docs/firmware-format.md).
- [Protocolo USB observado](docs/usb-protocol.md).
- [Reconstrução e testes do Penesas](docs/penesas.md).
- [Memória e limites ainda abertos](docs/memory.md).
- Ferramentas offline para inspecionar, comparar, reconstruir a candidata documentada e verificar capturas.
- [Plano de desenvolvimento](ROADMAP.md) e [como contribuir](CONTRIBUTING.md).

O código de reconstrução offline do Penesas gera um bloco de biblioteca. Separadamente, a prerelease V4 distribui um firmware completo experimental para o atualizador oficial e um monitor MIDI. Não há gerenciador público de efeitos.

## Começar

Python 3.10 ou superior. As ferramentas de inspeção usam somente a biblioteca padrão:

```sh
python -m pip install -e .
python -m matribox_lab inspect "local/matribox-v1.2.2.bin"
python -m matribox_lab compare "local/matribox-v1.1.4.bin" "local/matribox-v1.2.2.bin"
python -m unittest discover -s tests -v
```

Os arquivos em `local/` são fornecidos pelo próprio usuário. O histórico Git não inclui firmwares, ELF, bibliotecas geradas, presets ou capturas completas. O firmware experimental completo é disponibilizado separadamente em Releases. Os [hashes de referência](evidence/reference-inputs.json) identificam as entradas estudadas.

Para reproduzir a candidata **offline**, consulte [docs/penesas.md](docs/penesas.md). Esse processo foi conferido localmente e reproduz o hash da biblioteca sem compactação testada na pedaleira.

## Estado do projeto

| Área | Estado |
|---|---|
| Catálogo V1.1.4 / V1.2.2 | Decodificado e comparado |
| Atualização exclusiva da biblioteca | Sessões verificadas em USB e boot normal relatado |
| Penesas | Testado no aparelho pelo proprietário |
| 179 registros originais na candidata sem compactação | Idênticos byte por byte |
| Capacidade máxima para novos efeitos | Em investigação |
| Microfones integrados em cabinets e User IR | Testes físicos relatados; [escopo e limites](docs/cabinet-microphones.md) |
| Retorno SysEx do looper e undo/redo | Testado fisicamente; [protocolo e limites](docs/looper-sysex.md) |
| Gerenciador público de efeitos | Ainda não implementado |

As sessões iniciais usaram Windows 10 em VM. Em 17/10/2026, uma atualização completa da Lab V4 também foi confirmada diretamente no Windows 11, após selecionar o driver USB Audio Device nas interfaces MIDI dos modos normal e firmware. Veja [o procedimento e os limites](docs/windows11-update.md).

## English overview

Independent SONICAKE Matribox II Pro firmware and effect-catalog research. Integrated microphone filters were reported working on 20 factory cabinets and on user-imported IRs; see [scope and evidence](docs/cabinet-microphones.md). An experimental Valeton GP-200 Penesas port was tested on one physical unit. Offline tools reproduce the documented library from user-supplied firmware inputs; an experimental full firmware is now distributed separately as a prerelease, together with a looper SysEx monitor. Third-party components are not relicensed under MIT. See the source, evidence hashes and limitations before attempting to generalize the result.

## Licença e autoria

Mantido por [hurricaneabel](https://github.com/hurricaneabel). Código e documentação originais deste projeto sob [MIT](LICENSE). A licença não concede direitos sobre os firmwares ou algoritmos de terceiros usados como entradas locais. Projeto independente, sem afiliação ou aprovação declarada dos fabricantes.

# Atualizar a Matribox II Pro diretamente no Windows 11

Em **17/10/2026**, o proprietário confirmou a atualização completa do firmware **Lab V4** pelo programa oficial diretamente no Windows 11, após selecionar o driver **Dispositivo de Áudio USB / USB Audio Device** nas interfaces MIDI dos dois modos da pedaleira. Para esse procedimento, a VM deixou de ser necessária no computador testado.

A Sonicake reconhece problemas de comunicação USB MIDI no Windows 11 e publica um [procedimento oficial de troca de driver](https://www.sonicake.com/pages/stuck-updating-support). Este guia acrescenta um detalhe observado na Matribox II Pro: **modo normal e modo firmware usam identidades USB diferentes; é necessário conferir o driver em ambos**.

## Antes de começar

- Preserve backup de presets, arquivos IR/NAM e o firmware original para recuperação.
- Feche editor, frontend, DAW e monitores MIDI. Se houver VM, libere a Matribox para o Windows principal.
- Faça a troca de driver sem nenhuma atualização em andamento.
- O driver Sonicake USB ASIO 5.57.1 já estava instalado no ensaio e foi mantido. O guia da Sonicake orienta sua instalação antes da configuração; obtenha-o na [página oficial da Matribox II Pro](https://www.sonicake.com/pages/matribox-ii-pro-software-firmware-1).

## 1. Driver em modo normal

1. Conecte a pedaleira ao Windows 11 e deixe-a na tela normal dos presets.
2. Abra **Gerenciador de Dispositivos → Controladores de som, vídeo e jogos**.
3. Localize a interface MIDI da Matribox. Com o ASIO instalado, no ensaio ela apareceu como **Matribox II Pro Subdevice**.
4. Clique em **Atualizar driver → Procurar drivers no meu computador → Permitir que eu escolha em uma lista de drivers disponíveis no computador**.
5. Selecione **Dispositivo de Áudio USB / USB Audio Device** e conclua.
6. Reconecte o USB. Neste ensaio foi necessário também desligar e ligar a pedaleira para a consulta de estado voltar a responder.

O alvo é a interface MIDI indicada, não as entradas de alto-falante/linha na categoria de pontos de extremidade de áudio. Se a opção não aparecer entre os drivers compatíveis, interrompa e confira o guia oficial; não force um driver aleatório.

## 2. Driver em modo firmware — etapa separada

1. Coloque a pedaleira em **modo firmware**, mantendo o USB no Windows 11.
2. Volte a **Controladores de som, vídeo e jogos**. Nesse modo, no ensaio o dispositivo apareceu como **Matribox II PRO**, sem “Subdevice”.
3. Repita a seleção manual de **Dispositivo de Áudio USB / USB Audio Device**.
4. Reconecte o USB, mantendo o modo firmware, e reabra o atualizador somente após a porta estar disponível.

Trocar apenas o driver em modo normal não troca o do bootloader. No computador testado, os identificadores observados foram:

| Modo | Identidade observada | Driver após a troca |
|---|---|---|
| Normal, interface MIDI | VID `84EF`, PID `0282`, interface `MI_03` | `usbaudio`, INF `wdma_usb.inf` |
| Firmware/bootloader | VID `84EF`, PID `0283` | `usbaudio`, INF `wdma_usb.inf` |

Antes, ambas as interfaces MIDI usavam `USBMidi2` / `usbmidi2.inf`. O ASIO Sonicake foi mantido; não se alterou a configuração MIDI global do Windows.

## 3. Atualizar

1. Com o backup preservado, a pedaleira em modo firmware e os demais programas MIDI fechados, abra o atualizador oficial no Windows 11.
2. Selecione o **BIN completo** desejado. O arquivo usado no ensaio foi `QME-200_V1.2.2_LOOPER_UNDO_REDO_V4_MIC_EXPERIMENTAL.bin`, da [release Lab V4](https://github.com/hurricaneabel/matribox-ii-pro-effects-lab/releases/tag/v1.2.2-lab.4).
3. Inicie e deixe a atualização concluir sem desconectar ou desligar o equipamento.
4. Confira a inicialização, presets e áudio. Para usar o monitor do looper, mantenha modo normal e feche o atualizador para liberar a porta MIDI.

A página oficial atualmente orienta usar o software inicial V1.0.0 para atualizar firmware e a versão recente para uso normal. Os ensaios anteriores da pesquisa usaram o 1.2.0 na VM. A versão interna do programa utilizado neste novo ensaio Windows 11 não foi confirmada independentemente; não tratar o campo genérico ProductVersion do executável como prova dessa versão. Consulte as instruções atuais do fabricante ao escolher o atualizador.

Se a porta não abrir, feche outros programas MIDI e confira a atribuição USB. Os nomes das portas podem mudar após a troca do driver: liste-os novamente no seu programa. Falha de abertura de porta não exige, por si só, regravar firmware.

## Resultado e limites

- Host observado: **Windows 11 26H2, build 26300.9711**.
- Driver MIDI selecionado: `usbaudio`, versão `10.0.26100.9457`.
- ASIO mantido: Sonicake `5.57.1.32989`.
- Consulta normal do looper e identificação do bootloader passaram após a configuração.
- Atualização completa da Lab V4 confirmada pelo proprietário; SHA-256 BIN `00d1f50553be869af12fdf8d28533b13d477d126722f589f0e581c7e20060b41`.

O resultado é específico desta máquina/unidade. Não foi analisada captura USB desta atualização nem isolada a influência individual de driver, reconexão e reinicialização. Não comprova todos os Windows 11, atualizadores ou transmissores de biblioteca. A VM continua disponível como alternativa de recuperação, mas não foi usada nesta atualização bem-sucedida. Não foi necessário remover Windows Updates, alterar o registro ou modificar o programa do usuário.

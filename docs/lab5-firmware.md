Firmware completo experimental para **SONICAKE Matribox II Pro**, baseado no oficial **V1.2.2**. Esta Lab 5 reúne os recursos da Lab 4, as adições posteriores e o corretivo da navegação lateral da edição. **Não inclui alterações ou arquivos do programa matribox-sysex.**

> **Estado dos testes:** o proprietário relatou funcionamento dos efeitos mantidos, de Power LD/Juice30 OD, do indicador DSP e do Dark VIT. Os oito cabinets acrescentados depois do Dark VIT ainda não têm confirmação física individual registrada. O corretivo final das trocas laterais passou no emulador e **ainda aguarda confirmação física**. Por isso, esta publicação permanece uma pré-release experimental.

## Mudanças desde a Lab 4

- **DSP na própria pedaleira:** indicador na tela principal e na edição de efeitos; cadeia vazia apresentada como 0%, descontando a carga de base. Inclui consulta experimental de telemetria DSP por SysEx. Isso não equivale a uma certificação da capacidade máxima do processador.
- **Subclasses corrigidas:** adicionar modelos ao fim da biblioteca deixa de ocultar subclasses anteriores; modelos novos são classificados no grupo adequado.
- **Microfones:** padrão X/Y/Z em **50/50/50**, com Mic Type em **Off**, nos CABs e User IR. Presets existentes conservam suas posições salvas, inclusive valores 0.
- **Mais efeitos e amplificadores da GP-200**, listados abaixo, sem substituir os modelos de fábrica.
- **Oito cabinets adicionais além do Dark VIT de teste:** nove CABs portados no total, com microfones e seleção nativa; não ocupam os slots de importação de IR.
- **Cab Match** configurado para os amps relacionados abaixo.
- **Retirada de Bog BlueM, Bog RedV, Hold e Ice Delay GP**, com IDs/índices reservados para compatibilidade. A biblioteca e a navegação lateral da edição pulam esses modelos.
- **IDs e índices dos efeitos restantes preservados.** O corretivo não reordena Vibrato T, Dual Echo GP nem os demais modelos.

## Efeitos e amps portados — Valeton GP-200 V1.8.2

São **29 modelos adicionais mantidos**: os dez já presentes na Lab 4 e dezenove adicionados depois, contando os novos amplificadores. As descrições resumem as referências do manual; não garantem equivalência sonora integral com o aparelho doador.

### Boosts e drives

- **Penesas — Valeton GP-200:** overdrive de referência Klon Centaur, também utilizável como boost.
- **14 Boost — Valeton GP-200:** boost inspirado no Fortin Grind, voltado a dar definição e ataque ao amplificador.
- **Tube — Valeton GP-200:** overdrive inspirado no B. K. Butler Tube Driver, com graves e agudos ajustáveis.
- **Precise OD — Valeton GP-200:** referência Horizon Devices Precision Drive; inclui Attack e gate.
- **Empire OD — Valeton GP-200:** referência Analog.Man Prince of Tone, com três modos de operação.
- **Scream OD — Valeton GP-200:** variante da família Tube Screamer com controles adicionais Fat e Air.
- **Black Bass — Valeton GP-200:** pré/drive para baixo inspirado no Darkglass Microtubes B7K, com Blend e equalização.
- **Bass Hammer — Valeton GP-200:** pré para baixo inspirado no Aguilar Tone Hammer, com médios ajustáveis.

14 Boost fica em **DYN/Boost**; Black Bass e Bass Hammer em **DRV/Bass Drive**.

### Frequência, wah e equalização

- **Hammy — Valeton GP-200:** pitch shifter monofônico de referência Whammy, com posição atribuível à expressão.
- **Harmony 1 — Valeton GP-200:** harmonizador de uma voz, com tonalidade, modo e intervalo. No manual aparece como Harmonizer 1.
- **S-Wah — Valeton GP-200:** wah com faixa e ressonância ajustáveis.
- **Hyper EQ — Valeton GP-200:** equalizador gráfico de dez bandas.

### Modulação

- **Auto Swell — Valeton GP-200:** entrada gradual do volume, com ataque e curvas Line/Exp/Log. Inclui a correção de retrigger desenvolvida nesta pesquisa.
- **A-Chorus — Valeton GP-200:** chorus com caráter de modulação associado aos sons dos anos 1980.
- **Vibrato T — Valeton GP-200:** vibrato cuja profundidade responde à intensidade do sinal/palhetada.

### Delays

- **Digital Delay S — Valeton GP-200:** delay digital estéreo com relação de tempo entre canais e largura estéreo.
- **Tape Delay S — Valeton GP-200:** delay de fita estéreo com envelhecimento, saturação e modulação.
- **Broken Delay — Valeton GP-200:** delay de repetições fragmentadas e cortes, para efeitos de glitch.
- **Ambience 1 — Valeton GP-200:** variante de delay ambiente, com repetição, modulação e tom ajustáveis.
- **Ambience 2 — Valeton GP-200:** segunda variante de delay ambiente. A tabela do manual é inconsistente entre essas entradas; a descrição foi mantida genérica.
- **Dual Echo GP — Valeton GP-200:** dois delays com Mix, Time e Feedback separados, além de sincronização independente. Mantido como variante para comparação com Eko D; não é apresentado como algoritmo inteiramente exclusivo.

**Level**, nos delays que possuem esse controle, regula a saída total: 0 silencia, 50 mantém o ganho unitário e 100 dobra a amplitude. **Mix** regula a proporção entre som direto e delay. Esse comportamento não foi alterado nesta revisão.

### Reverbs

- **Tube Spring — Valeton GP-200:** reverb de mola de referência a uma unidade com acionamento valvulado.
- **Amp Spring — Valeton GP-200:** reverb de mola de referência ao módulo de um amplificador combo com circuito de estado sólido.

### Amplificadores

- **Power LD — Valeton GP-200:** referência ENGL Powerball II, canal 4; modelo de alto ganho.
- **Juice30 OD — Valeton GP-200:** referência Orange AD30, canal de drive.
- **Dark Vibra — Valeton GP-200:** referência Fender Vibroverb, circuito 6G16.
- **Silver Twin — Valeton GP-200:** referência Fender Silverface Twin Reverb.
- **Bad-KT CL — Valeton GP-200:** referência Bad Cat Hot Cat 30, canal limpo.
- **Bad-KT OD — Valeton GP-200:** referência Bad Cat Hot Cat 30, canal de drive.

## Cabinets portados — Valeton GP-200 V1.8.2

São **coeficientes de cabinet da GP-200**, integrados ao convolver da Matribox e à camada de microfones já adaptada. Não representam um port de todo o motor de convolução da GP-200.

| Cabinet | Origem | Referência resumida do manual |
|---|---|---|
| Dark VIT | Valeton GP-200 | Fender Vibrolux, 1x12 |
| ROUT | Valeton GP-200 | Carr Rambler, 1x12 |
| Bad-KT | Valeton GP-200 | Hot Cat, 1x12 |
| TOM OPEN | Valeton GP-200 | Swart Atomic Space, 1x12 |
| ACE | Valeton GP-200 | Morgan AC-20 Deluxe, 1x12 |
| BOUTI | Valeton GP-200 | Cabinet customizado, 2x12 |
| Freed | Valeton GP-200 | Fryette Deliverance, 2x12 |
| DB Rock | Valeton GP-200 | Two-Rock, 2x12 |
| TRP | Valeton GP-200 | Hughes & Kettner Triamp, 4x12 |

Os **61 cabinets de fábrica permanecem**; a lista passa a ter **70 CABs**, com os mesmos 20 slots User IR e 10 slots NAM. Dark VIT conserva o ID e o índice da versão de teste anterior.

### Cab Match

- **Bad-KT CL / Bad-KT OD → Bad-KT.**
- **Dark Vibra → Dark VIT**, seguindo a associação do firmware GP-200. O manual descreve os dois com referências diferentes; essa associação não afirma que Vibroverb e Vibrolux sejam o mesmo amplificador.
- **Power LD → Eng 4x12** de fábrica.
- **Juice30 OD → Tanger 4x12** de fábrica.

Os outros cabinets novos ficam disponíveis para escolha manual. As demais associações de fábrica são preservadas. Cab Match deve estar habilitado e segue a regra nativa de associação com um bloco CAB existente na cadeia.

## Microfones — origem: Hotone Ampero Mini V2.2

A camada de filtro de microfone/posição foi extraída da **Hotone Ampero Mini V2.2** e adaptada ao processamento de CABs e User IR da Matribox. Há seleção de microfone e posições X/Y/Z; não é uma reprodução da interface gráfica da Ampero Mini nem uma garantia de equivalência acústica integral entre os aparelhos.

O padrão é **Mic Type Off e X/Y/Z=50**. Os ajustes de presets salvos são preservados. A importação de IR não foi alterada.

## Looper SysEx preservado

Mantém o trabalho desenvolvido neste projeto: retorno do estado do looper, Auto Rec, Drum Sync, Rec Level, Pre/Post, Play Volume e eventos de undo/redo. O envio ocorre por mudanças, sem heartbeat contínuo. Esses recursos são alterações deste projeto no firmware Matribox, não ports da GP-200.

## Modelos retirados e compatibilidade

- **Bog BlueM / Bog RedV:** retirados por redundância sonora relatada com os Bogs existentes.
- **Hold:** retirado por escolha do proprietário.
- **Ice Delay GP:** retirado após falha física com perda persistente de áudio. Não deve ser usado nem tratado como port funcional.

**Ice Delay, Bog XT Blue e Bog XT Red originais da Matribox permanecem.** Os algoritmos retirados não continuam escondidos no firmware: pequenos registros e uma rotina de passagem direta reservam seus IDs/índices. Presets antigos que ainda apontem para eles não carregam outro efeito naquele endereço. Essa reserva de compatibilidade não reutiliza os buffers e algoritmos retirados.

O corretivo final também trata as trocas laterais da edição: **A-Chorus ↔ Vibrato T** e **Ambience 2 ↔ Dual Echo GP**, pulando os registros aposentados. Os Bogs retirados não são alcançados no fim de AMP.

## Baixar e instalar

1. Baixe o **ZIP da Lab 5**, confira `SHA256SUMS.txt` e extraia o BIN completo.
2. Preserve seus backups de presets, arquivos IR/NAM e o firmware anterior confirmado.
3. Coloque a **Matribox II Pro em modo firmware** e use o atualizador oficial. Aguarde a conclusão e a reinicialização.
4. O ZIP contém `INSTALACAO.txt` com os testes prioritários. Não é necessário instalar os pacotes de teste anteriores.

No Windows 11, siga o [procedimento de driver dos modos normal e firmware](https://github.com/hurricaneabel/matribox-ii-pro-effects-lab/blob/main/docs/windows11-update.md). Não use em Matribox II ou outros modelos.

**BIN SHA-256:** `ff3cded00a1d7d0ef36f67d7da0627abada64c1c17016702cb5f97c4e984a800`.

## Validação e limites

O corretivo final passou em **610 trocas de avançar/voltar**, incluindo limites de listas, **45 listas nativas**, **506 seleções** e **305 verificações da seleção atual** no emulador. Biblioteca, DSP e ambos os blocos de recursos são idênticos ao pacote de nove cabinets anterior; o corretivo modifica apenas 69 bytes do programa principal, além do checksum externo.

Na expansão dos cabinets, foram conferidos os ponteiros dos nove IRs, processamento com microfones, 100 operações de salvar/restaurar recursos, 209 de modelos DSP, preservação de posições e Cab Match ligado/desligado. Alguns componentes de armazenamento, widgets e admissão de memória foram modelados nos testes. Não se executou o boot completo ou todo o touchscreen físico no emulador.

A capacidade máxima de expansão não foi estabelecida; os limites nativos de memória não foram aumentados. Algumas opções de parâmetros ainda usam rótulos numéricos. Tempos do emulador não são apresentados como medidas de custo DSP físico.

Fontes: [manual oficial GP-200 V1.8.0](https://res.valeton.net/Uploads/wp/download/1768360642746.GP-200_Online%C2%A0Manual_EN_Firmware%20V1.8.0.pdf), firmwares GP-200 V1.8.2 e Ampero Mini V2.2 usados como entradas locais, e os resultados desta pesquisa. As descrições acima são resumos em português.

Projeto independente, sem afiliação ou aprovação dos fabricantes. A licença MIT do repositório cobre o código e a documentação originais do projeto; não relicencia firmware ou componentes de terceiros.

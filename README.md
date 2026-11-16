# Bust A Move 2 JP — Native Recompilation

**Português (Brasil)** | [**English**](README_EN.md)

**Projeto experimental de recompilação nativa para Windows**  
**Versão:** v0.1 (código-fonte) · **Status:** em desenvolvimento (experimental) · **Mantenedor:** Ahrian · **Plataforma:** Windows · **Jogo-alvo:** *Bust A Move 2: Dance Tengoku Mix* (PlayStation japonês, SLPM-86219)

> **Este repositório não contém o jogo.** Aqui são distribuídos apenas ferramentas, configurações e modificações do [PSXRecomp](https://github.com/RetroPortingToolKit/psxrecomp). Cada usuário deve fornecer, de maneira legítima, seus próprios arquivos compatíveis do disco original e gerar a compilação **localmente**.

**English summary:** An unofficial, experimental Windows native-recompilation project for the Japanese PlayStation release of *Bust A Move 2: Dance Tengoku Mix* (SLPM-86219), based on PSXRecomp. **No game files, disc images, assets, original executable, generated game code, or precompiled game binaries are distributed.** Users must provide their own lawfully obtained, compatible disc files and build locally. See [Licenses & attribution](#licenças-e-créditos) below.

---

## Índice

- [Sobre o projeto](#sobre-o-projeto)
- [O que a v0.1 oferece](#o-que-a-v01-oferece)
- [Requisitos e compatibilidade](#requisitos-e-compatibilidade)
- [Instalação e primeira execução](#instalação-e-primeira-execução)
- [Onde ficam os arquivos pessoais](#onde-ficam-os-arquivos-pessoais)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Estado atual e limitações](#estado-atual-e-limitações)
- [Roadmap — próximas etapas](#roadmap--próximas-etapas)
- [Problemas comuns](#problemas-comuns)
- [Segurança e conferência do pacote](#segurança-e-conferência-do-pacote)
- [Licenças e créditos](#licenças-e-créditos)
- [Contribuições](#contribuições)

## Sobre o projeto

O objetivo deste projeto é investigar a **recompilação nativa de um jogo original de PlayStation para Windows**, utilizando o framework PSXRecomp como base. O trabalho explora a integração do executável gerado com um runtime moderno, renderização OpenGL e técnicas experimentais de apresentação de quadros.

A prioridade é preservar o comportamento do jogo, especialmente **música, ritmo e julgamento dos comandos**, enquanto se estudam melhorias visuais e de compatibilidade. Trata-se de uma iniciativa técnica e comunitária **não oficial**, em desenvolvimento.

O projeto **não é um remake**, não substitui uma cópia legítima do jogo e não oferece downloads de material comercial.

> 🚧 **Projeto em desenvolvimento:** a v0.1 é uma versão inicial e experimental. **Selecionar livremente uma taxa de apresentação de até 360 FPS e jogar online com rollback netcode são objetivos futuros; nenhum desses recursos está disponível ou garantido na v0.1.** Consulte o [roadmap](#roadmap--próximas-etapas).

## O que a v0.1 oferece

| Componente | Situação na v0.1 |
| --- | --- |
| Assistente gráfico para Windows | Código-fonte C# incluído; compilação local |
| Preparação por linha de comando | Script Python incluído |
| Download do framework | Automatizado e fixado em um commit específico |
| Configuração da edição japonesa | Incluída para **SLPM-86219** |
| Código de runtime modificado | Incluído em `runtime-overrides/` |
| Renderização | Runtime configurado para **OpenGL** |
| Geração de quadros | **Experimental**; execução padrão usa `redraw` |
| Reprojeção e proteções visuais | Código experimental presente, **não ativado como modo padrão de execução** |
| Seleção de taxa de apresentação (até 360 FPS) | **Planejada; ainda não disponível** |
| Multiplayer online com rollback netcode | **Planejado; ainda não disponível** |
| Jogo, BIOS e executável pronto | **Não incluídos** |

**Importante:** frequência de atualização do monitor, taxa de quadros do jogo original e quantidade de quadros intermediários gerados são coisas diferentes. Não há promessa de **360 FPS únicos**, ausência de artefatos ou redução garantida de latência.

## Requisitos e compatibilidade

- **Windows de 64 bits**.
- **Python 3.11 ou superior**, acessível por `py -3` ou `python`.
- **Git for Windows** e acesso à internet para obter o PSXRecomp e seus submódulos.
- Ferramentas e dependências de compilação exigidas pelo **PSXRecomp**, incluindo a toolchain C/C++/CMake correspondente ao ambiente Windows.
- Espaço livre em disco para dependências, código gerado e compilação.
- Arquivo **`.cue` da edição japonesa SLPM-86219**, acompanhado dos arquivos `.bin` aos quais ele faz referência, obtidos legitimamente pelo próprio usuário.
- Para compilar o **assistente gráfico**, o compilador C# (`csc.exe`) do **.NET Framework 4.x** no caminho utilizado pelo script `source/build-assistant.cmd`.

A configuração fornecida é específica dessa edição japonesa. **Outras regiões, versões ou revisões do disco não são declaradas compatíveis.** A preparação usa informações de layout e identificadores específicos da edição-alvo.

## Instalação e primeira execução

### Opção A — Pelo Python (recomendada para diagnosticar erros)

**1.** Baixe o código-fonte deste repositório e extraia-o para uma pasta de sua escolha. Não coloque os arquivos do jogo dentro da pasta do repositório.

**2.** Verifique se Python e Git estão disponíveis no PowerShell:

```powershell
py -3 --version
git --version
```

**3.** No PowerShell, abra a pasta do repositório e execute a preparação, substituindo o exemplo pelo caminho **real** do seu `.cue`:

```powershell
py -3 .\source\prepare.py prepare --disc 'D:\MeusJogos\BAM2JP.cue'
```

A preparação baixa o PSXRecomp no commit fixado, inicializa os submódulos, aplica os arquivos de runtime deste projeto e tenta gerar e compilar a versão **pessoal** do jogo. A primeira execução requer internet e pode exigir componentes adicionais da toolchain de compilação.

**4.** Se a preparação terminar com sucesso, inicie a compilação pessoal:

```powershell
py -3 .\source\prepare.py play
```

Se a compilação falhar, mantenha a mensagem de erro e consulte [Problemas comuns](#problemas-comuns). Não redistribua os arquivos temporários ou gerados.

### Opção B — Assistente gráfico para Windows

O repositório distribui o **código-fonte**, não um `Assistente_BAM2.exe` pronto.

**1.** Dentro da pasta do repositório, execute:

```cmd
source\build-assistant.cmd
```

**2.** Se o compilador C# estiver disponível, será criado localmente o arquivo `Assistente_BAM2.exe` na raiz do projeto.

**3.** Abra o assistente, selecione seu arquivo `.cue`, leia os avisos e confirme que possui a cópia apropriada. Clique em **“1. Preparar minha cópia”**.

**4.** Após o processo concluir com sucesso, clique em **“2. Jogar”**.

O assistente usa o mesmo script Python da opção A. O programa não cria imagens de CDs físicos e não baixa o jogo.

## Onde ficam os arquivos pessoais

Por padrão, a preparação utiliza a pasta:

```text
%LOCALAPPDATA%\BAM2RecompTest\v0.1
```

É nessa área que ficam o framework baixado, os arquivos gerados a partir do disco, o build pessoal, os saves e os logs. O arquivo de disco original permanece no caminho escolhido pelo usuário.

**Não envie essa pasta ao GitHub e não compartilhe o executável pessoal, dados extraídos, saves, caches ou código gerado do jogo.** O repositório público contém somente o material descrito na seção seguinte.

## Estrutura do repositório

```text
.
├── README.md                         # Apresentação e instruções (português)
├── README_EN.md                      # Documentação em inglês
├── LEIA-ME.txt                       # Instruções resumidas
├── RELEASE_CHECKLIST.md              # Checklist para publicação
├── VALIDACAO.txt                     # Histórico e limites dos testes
├── framework.json                    # Origem e commit do PSXRecomp
├── manifest-sha256.json              # Integridade dos arquivos públicos
├── source/
│   ├── Assistente.cs                  # Interface gráfica em C#
│   ├── build-assistant.cmd            # Compilação local do assistente
│   └── prepare.py                     # Preparar / executar build pessoal
├── template/
│   ├── game.toml                      # Configuração SLPM-86219
│   ├── CMakeLists.txt                 # Configuração CMake
│   └── seeds/ghidra_funcs.txt         # Lista de endereços numéricos
├── runtime-overrides/                # Arquivos modificados do PSXRecomp
├── licenses/                         # Licenças e atribuições
├── tools/check_publication.py        # Auditoria antes da publicação
└── .github/workflows/                 # Verificação automatizada
```

A lista `template/seeds/ghidra_funcs.txt` contém **588 endereços numéricos**, obtidos durante a análise técnica do executável original; não contém instruções MIPS. Esses metadados não são um substituto para o jogo, mas seu uso e redistribuição também exigem atenção às leis aplicáveis.

## Estado atual e limitações

**v0.1 é experimental.** Seu propósito é disponibilizar uma base reproduzível para investigação e desenvolvimento, não anunciar um port finalizado.

- A execução padrão configurada por `source/prepare.py` utiliza `PSX_FRAME_GEN_METHOD=redraw`. A **reprojeção** permanece experimental e pode apresentar artefatos visuais.
- A taxa de quadros efetivamente obtida depende do jogo, hardware, renderizador e configuração. Uma tela de 360 Hz não implica 360 quadros únicos por segundo. **A seleção de metas de FPS pelo usuário ainda é um objetivo do roadmap, não um recurso desta versão.**
- Não há garantia de funcionamento em todas as máquinas, revisões do Windows ou GPUs.
- O registro em [`VALIDACAO.txt`](VALIDACAO.txt) descreve testes históricos em ambiente de desenvolvimento; **a instalação a partir do pacote público ainda não foi validada integralmente em um Windows limpo**.
- Não foi anunciada validação completa de músicas inteiras, sincronização e julgamento em todos os cenários.
- **Não existe multiplayer online ou rollback netcode funcional na v0.1.**
- A recompilação depende das ferramentas e licenças do PSXRecomp e das dependências obtidas durante a instalação.

Para saber o que já foi verificado antes de uma release, consulte [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md).

## Roadmap — próximas etapas

O plano abaixo apresenta **intenções de desenvolvimento**, não funcionalidades concluídas ou compromissos de prazo. As prioridades podem mudar de acordo com testes, limitações técnicas e contribuições da comunidade.

| Etapa | Objetivo | Situação |
| --- | --- | --- |
| 1. Base nativa para Windows | Consolidar a compilação local, o assistente e a compatibilidade com a edição japonesa SLPM-86219 | **Base experimental na v0.1** |
| 2. Qualidade e estabilidade | Investigar regressões visuais, melhorias do renderizador, áudio, sincronização musical e resposta dos comandos | **Em desenvolvimento** |
| 3. Taxa de apresentação configurável | Permitir ao usuário escolher a meta de apresentação, com opções até **360 FPS** em hardware compatível, usando técnicas de geração de quadros quando necessárias | **Planejado** |
| 4. Multiplayer online | Investigar partidas entre jogadores pela rede, com **rollback netcode**, predição de entradas, snapshots e ressímulação | **Planejado / pesquisa futura** |

### Meta de apresentação: até 360 FPS

A intenção é oferecer configurações como **30, 60, 120, 144, 165, 240 e 360 FPS**, quando tecnicamente viáveis. Esses valores são **metas futuras de apresentação visual**, não resultados já alcançados ou certificados. O objetivo é melhorar a fluidez percebida **sem acelerar músicas, animações lógicas ou janelas de julgamento**. O ritmo da simulação original e a apresentação de quadros adicionais devem continuar separados.

Mesmo após a implementação, a taxa efetiva dependerá de GPU, CPU, driver, tela e complexidade de cada cena. A geração de quadros pode introduzir artefatos ou latência; sua qualidade e estabilidade precisarão ser demonstradas antes de qualquer anúncio de suporte definitivo a 360 FPS.

### Multiplayer online com rollback netcode

Uma meta de longo prazo é permitir **jogar online com outras pessoas**, utilizando rollback netcode. Para isso, será necessário investigar determinismo da simulação, sincronização de entradas e música, captura/restauração rápida de estado, predição de comandos remotos e ressímulação segura sob latência real.

**Rollback netcode não deve ser confundido com o defeito visual de “quadro antigo reaparecendo” investigado durante os experimentos de reprojeção:** são assuntos diferentes. A v0.1 **não possui infraestrutura de partidas online nem rollback netcode**.

Não há data de lançamento confirmada para esses recursos. Contribuições e resultados de testes poderão orientar o planejamento.

## Problemas comuns

| Sintoma | O que conferir |
| --- | --- |
| `py` ou `python` não encontrado | Instale Python 3.11+ e confira o PATH |
| `git` não encontrado | Instale Git for Windows e reabra o terminal |
| Arquivo `.cue` recusado | Confira a edição japonesa **SLPM-86219**, os arquivos `.bin` referenciados e o caminho informado |
| Falha durante `generate` ou `rebuild` | Verifique a toolchain do PSXRecomp, as dependências e a saída completa do PowerShell |
| `csc.exe` não encontrado | Instale os componentes necessários do .NET Framework 4.x ou use a opção pelo Python |
| Comando `play` falha | Execute primeiro `prepare` com sucesso; não apague a pasta de instalação pessoal |
| Artefatos ou desempenho inconsistente | A geração de quadros é experimental; registre as condições e a mensagem de erro antes de relatar |

Ao relatar um problema, inclua a versão do Windows, GPU, etapa em que falhou e **mensagens técnicas relevantes**, removendo caminhos pessoais, e-mails, dados do disco e informações privadas. Não anexe o jogo nem conteúdos extraídos dele.

## Segurança e conferência do pacote

Antes de publicar alterações ou distribuir código, execute **na pasta do repositório**:

```powershell
py -3 .\tools\check_publication.py
```

O script utiliza uma lista de arquivos permitidos, verifica **tamanho e SHA-256** conforme `manifest-sha256.json` e bloqueia formatos e diretórios não destinados à distribuição. O workflow do GitHub Actions também verifica os arquivos rastreados nos commits.

**Observação:** sempre que algum arquivo público for alterado, o manifesto precisa ser atualizado de forma controlada antes do commit. A verificação automática não comprova autoria, licença, segurança do código ou ausência absoluta de material protegido.

## Licenças e créditos

Este repositório **não possui uma licença única para todo o conteúdo**. Consulte os arquivos de cada componente antes de reutilizá-lo.

| Componente | Origem / licença |
| --- | --- |
| Assistente, scripts e documentação original abrangidos pelos avisos | **MIT**, com atribuição pública **Ahrian**, conforme [`licenses/assistant-MIT.txt`](licenses/assistant-MIT.txt) e [`licenses/NOTICE.txt`](licenses/NOTICE.txt) |
| Arquivos modificados do PSXRecomp em `runtime-overrides/` | **PolyForm Noncommercial 1.0.0** e avisos adicionais aplicáveis; **não** são relicenciados sob MIT |
| Algoritmo/filtro xBR adaptado no renderizador | Trabalho atribuído a **Hyllian**, sob MIT; veja [`licenses/xBR-Hyllian-MIT.txt`](licenses/xBR-Hyllian-MIT.txt) |
| Jogo, marcas, música, personagens e demais assets | Direitos reservados aos respectivos titulares; **não distribuídos nem licenciados por este projeto** |

**Créditos:**

- **Ahrian** — mantenedor do projeto e da adaptação pública; assistente e documentação desenvolvidos com auxílio do **OpenAI Codex/ChatGPT**.
- **Matthew Stanley e contribuidores do PSXRecomp** — framework de recompilação e runtime. [Projeto upstream](https://github.com/RetroPortingToolKit/psxrecomp), [commit fixado](https://github.com/RetroPortingToolKit/psxrecomp/tree/b263b8552e5b8838b317f8921dfde8b6aca97904), [permissões adicionais](https://github.com/RetroPortingToolKit/psxrecomp/blob/b263b8552e5b8838b317f8921dfde8b6aca97904/PERMISSIONS.md) e [atribuições de terceiros](https://github.com/RetroPortingToolKit/psxrecomp/blob/b263b8552e5b8838b317f8921dfde8b6aca97904/THIRD_PARTY_ATTRIBUTION.md).
- **Hyllian** — trabalho original do algoritmo xBR, conforme licença e avisos preservados.

A referência a nomes comerciais identifica apenas o jogo-alvo. **Este projeto não possui afiliação, autorização ou endosso declarado dos titulares de *Bust A Move 2* ou de suas marcas.** Direitos de uso, cópia, extração e interoperabilidade variam conforme a jurisdição e não são concedidos por este repositório.

## Contribuições

Relatórios técnicos, correções documentais e sugestões são bem-vindos por meio das ferramentas do GitHub, quando habilitadas. Antes de enviar alterações:

1. Não inclua ROMs, ISOs, BIN/CUE, BIOS comercial, assets, dumps, código gerado do jogo ou executáveis recompilados.
2. Respeite as licenças de cada componente e preserve as atribuições de terceiros.
3. Verifique `RELEASE_CHECKLIST.md` e execute `py -3 .\tools\check_publication.py`.
4. Descreva o ambiente de testes e evite alegar recursos ou desempenho que não tenham sido confirmados.

---

**Projeto experimental, não comercial e não oficial.** Obrigado por apoiar pesquisa, preservação e desenvolvimento técnico responsável.

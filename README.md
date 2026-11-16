# Bust A Move 2 JP — Native Recomp (v0.1 experimental)

Projeto comunitário **não oficial** de ferramentas, configurações e modificações do
[PSXRecomp](https://github.com/RetroPortingToolKit/psxrecomp) para *Bust A Move 2:
Dance Tengoku Mix* (PlayStation japonês, **SLPM-86219**).

**Este repositório não contém o jogo.** Não inclui ISO/BIN/CUE, executável
original de PlayStation, código C gerado a partir do jogo, BIOS comercial,
assets, vídeos, músicas, texturas, capa, executável nativo recompilado nem
caches derivados do conteúdo do disco. Os usuários fornecem os próprios
arquivos de disco compatíveis, de forma legítima, e geram o resultado apenas
em seus computadores. Possuir uma cópia não substitui o cumprimento das leis
aplicáveis de copyright, extração e interoperabilidade na sua jurisdição.

## O que está incluído

- `source/`: assistente Windows em C# e script Python de instalação pessoal;
- `template/`: configuração, CMake e lista de endereços numéricos usada pelo recompiler;
- `runtime-overrides/`: **arquivos completos modificados do PSXRecomp**,
  distribuídos sob a licença aplicável do framework, **não sob MIT**;
- `licenses/`: licenças, atribuições e avisos de origem;
- `tools/check_publication.py`: auditoria de arquivos antes de cada commit/release.

A lista `template/seeds/ghidra_funcs.txt` contém somente endereços numéricos;
ela não contém instruções MIPS. É um metadado derivado da análise da edição
japonesa. Se sua política de publicação não aceitar esses metadados,
**não publique este pacote sem adaptar o gerador para criá-los localmente**.

## Requisitos

Windows 64 bits; Python 3.11+ no PATH (ou `py -3`); Git for Windows; acesso à
internet; compilador/toolchain exigidos pelo PSXRecomp, espaço livre para a
compilação e imagem `.cue` da edição japonesa acompanhada dos `.bin` referidos.
A configuração é específica de **SLPM-86219** e não aceita outras regiões.

## Começo rápido (sem EXE pré-compilado)

No PowerShell, dentro da pasta deste repositório:

```powershell
py -3 .\source\prepare.py prepare --disc 'D:\MinhaColecao\BAM2JP.cue'
py -3 .\source\prepare.py play
```

Como alternativa, para compilar a interface gráfica localmente, use
`source\build-assistant.cmd` no Windows (necessita o compilador C# do .NET
Framework 4.x disponível no caminho usado por esse script). Depois abra
`Assistente_BAM2.exe`, que será criado **somente no seu computador**.

O assistente guarda os arquivos baixados, dados de disco e binários gerados
fora do repositório, normalmente em
`%LOCALAPPDATA%\BAM2RecompTest\v0.1`. **Nunca distribua essa pasta.**

O PSXRecomp é fixado ao commit informado em `framework.json`; o preparo baixa
o framework e suas dependências e aplica os arquivos de `runtime-overrides/`.
A compilação e o jogo só foram verificados em ambiente pré-configurado; não há
garantia de funcionamento em instalação Windows limpa. Os 360 Hz são um
objetivo de desenvolvimento, **não uma taxa de FPS garantida**.

## Licenciamento e terceiros

- Os arquivos modificados de `runtime-overrides/` pertencem ao ecossistema
  PSXRecomp e continuam sob **PolyForm Noncommercial 1.0.0**, com avisos em
  `licenses/psxrecomp-LICENSE.txt` e `licenses/NOTICE.txt`.
- PSXRecomp: copyright © 2026 **Matthew Stanley** e demais contribuidores
  identificados pelos respectivos avisos. Veja o
  [repositório original](https://github.com/RetroPortingToolKit/psxrecomp),
  o [commit usado](https://github.com/RetroPortingToolKit/psxrecomp/tree/b263b8552e5b8838b317f8921dfde8b6aca97904),
  as [atribuições de terceiros](https://github.com/RetroPortingToolKit/psxrecomp/blob/b263b8552e5b8838b317f8921dfde8b6aca97904/THIRD_PARTY_ATTRIBUTION.md)
  e as [permissões adicionais](https://github.com/RetroPortingToolKit/psxrecomp/blob/b263b8552e5b8838b317f8921dfde8b6aca97904/PERMISSIONS.md).
- O assistente e os componentes próprios listados em `licenses/NOTICE.txt`
  são oferecidos sob MIT (`licenses/assistant-MIT.txt`) na extensão dos direitos
  de seus mantenedores. Foram preparados com auxílio de OpenAI Codex/ChatGPT.
  A atribuição coletiva é provisória; antes de anunciar autoria individual,
  confirme o titular e as permissões de quaisquer contribuidores.
- O filtro de textura xBR utilizado pelo renderizador é uma adaptação de
  trabalho de **Hyllian** (MIT). O aviso integral está em
  `licenses/xBR-Hyllian-MIT.txt`; os créditos do framework estão em
  `licenses/NOTICE.txt`. A MIT não relicencia os arquivos do runtime.
- Marcas, personagens, músicas e demais direitos do jogo são de seus
  respectivos titulares. Este projeto não é afiliado nem endossado por eles.

## Revisão de publicação

```powershell
py -3 .\tools\check_publication.py
```

A verificação exige que todos os arquivos estejam numa lista permitida,
compara os SHA-256 com `manifest-sha256.json` e recusa arquivos de disco,
binários e pastas de build. **Ela não substitui revisão humana nem auditoria
jurídica.** Veja `RELEASE_CHECKLIST.md` antes de publicar qualquer release.

Para mais detalhes em português: `LEIA-ME.txt`.

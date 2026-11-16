"""Personal-disc builder. Never writes extracted or generated game data into the package.

BAM2: habilita o launcher do PSXRecomp sem alterar as opcoes de desempenho
usadas anteriormente pelo assistente ao iniciar o jogo.
"""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

PACKAGE = Path(__file__).resolve().parents[1]
PIN = json.loads((PACKAGE / 'framework.json').read_text(encoding='utf-8'))

UI_REPOSITORY = 'https://github.com/RetroPortingToolKit/recomp-ui.git'


def run(args, cwd, env):
    print('> ' + subprocess.list2cmdline([str(x) for x in args]), flush=True)
    subprocess.run([str(x) for x in args], cwd=cwd, env=env, check=True)


def ensure_recomp_ui(workspace, env):
    """Mantem a copia local existente; so clona quando ainda nao existe."""
    ui = workspace / 'recomp-ui'
    if (ui / 'recomp_ui.cmake').is_file():
        print('recomp-ui existente: ' + str(ui), flush=True)
        return ui
    if ui.exists():
        raise RuntimeError(
            'recomp-ui ja existe, mas falta recomp_ui.cmake: ' + str(ui)
        )
    run(['git', 'clone', UI_REPOSITORY, ui], workspace, env)
    if not (ui / 'recomp_ui.cmake').is_file():
        raise RuntimeError('Clone de recomp-ui incompleto: ' + str(ui))
    return ui


def enable_launcher_in_generated_cmake(workspace):
    """Corrige a linha FORCE gerada pela CLI antes de configurar o build.

    Apenas passar -DPSX_RECOMP_UI=ON nao basta: o CMakeLists.txt gerado
    pelo assistente faz `set(PSX_RECOMP_UI OFF CACHE BOOL ... FORCE)`.
    """
    cmake_file = workspace / 'CMakeLists.txt'
    if not cmake_file.is_file():
        raise RuntimeError('CMakeLists.txt nao foi gerado: ' + str(cmake_file))

    source = cmake_file.read_bytes().decode('utf-8')
    pattern = re.compile(
        r'(?mi)^([ \t]*set[ \t]*\([ \t]*PSX_RECOMP_UI[ \t]+)'
        r'(?:OFF|ON)([ \t]+CACHE[ \t]+BOOL[ \t]+[^\r\n]*?\bFORCE[ \t]*\)[ \t]*)(\r?)$'
    )
    if len(pattern.findall(source)) != 1:
        raise RuntimeError(
            'Nao encontrei uma unica linha PSX_RECOMP_UI ... FORCE no '
            'CMakeLists.txt gerado. Nao vou alterar o projeto automaticamente.'
        )

    updated = pattern.sub(lambda m: m.group(1) + 'ON' + m.group(2) + m.group(3), source)
    if updated != source:
        cmake_file.write_bytes(updated.encode('utf-8'))
    print('CMakeLists.txt: PSX_RECOMP_UI=ON (linha FORCE corrigida)', flush=True)


def check_launcher_cache(workspace):
    """Nunca anuncia launcher habilitado quando o cache estiver OFF."""
    cache = workspace / 'build' / 'CMakeCache.txt'
    if not cache.is_file():
        raise RuntimeError('Build concluiu sem CMakeCache.txt: ' + str(cache))
    matches = re.findall(
        r'(?m)^PSX_RECOMP_UI:BOOL=(ON|OFF)[ \t]*$',
        cache.read_text(encoding='utf-8', errors='replace')
    )
    if matches != ['ON']:
        raise RuntimeError(
            'Launcher nao habilitado no CMakeCache.txt: '
            + (', '.join(matches) if matches else 'opcao ausente')
        )
    print('CMakeCache.txt: PSX_RECOMP_UI:BOOL=ON', flush=True)


def prepare(disc, workspace, cache=None, build=True):
    if sys.version_info < (3, 11):
        raise RuntimeError('Instale Python 3.11 ou posterior.')
    if not shutil.which('git'):
        raise RuntimeError('Instale Git for Windows e reabra o assistente.')

    disc = Path(disc).resolve(strict=True)
    if disc.suffix.lower() != '.cue':
        raise ValueError(
            'Selecione o .cue da edicao japonesa SLPM-86219, '
            'com os .bin correspondentes.'
        )
    workspace = Path(workspace).resolve()
    if workspace == PACKAGE or PACKAGE in workspace.parents:
        raise ValueError('A instalacao pessoal deve ficar fora da pasta distribuivel.')
    workspace.mkdir(parents=True, exist_ok=True)

    env = {k: v for k, v in os.environ.items() if not k.startswith('PSX_')}
    env.update(
        CMAKE_BUILD_PARALLEL_LEVEL='2',
        PSXRECOMP_AOT_WORKERS='2',
        PYTHONUTF8='1',
        PYTHONUNBUFFERED='1',
    )

    framework = workspace / 'psxrecomp'
    if not framework.exists():
        run(['git', 'clone', '--no-checkout', cache or PIN['repository'], framework],
            workspace, env)
        run(['git', 'checkout', '--detach', PIN['commit']], framework, env)
        if cache:
            run(['git', 'remote', 'set-url', 'origin', PIN['repository']],
                framework, env)

    head = subprocess.check_output(
        ['git', 'rev-parse', 'HEAD'], cwd=framework, text=True
    ).strip()
    if head != PIN['commit']:
        raise RuntimeError(
            'Framework em versao diferente; use outra pasta de instalacao pessoal.'
        )

    # Somente dependencias do checkout fixado: nada e extraido no repositorio.
    run(['git', 'submodule', 'update', '--init', '--recursive'], framework, env)

    for p in (PACKAGE / 'runtime-overrides').rglob('*'):
        if p.is_file():
            dest = framework / p.relative_to(PACKAGE / 'runtime-overrides')
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dest)

    for p in (PACKAGE / 'template').rglob('*'):
        if p.is_file():
            dest = workspace / p.relative_to(PACKAGE / 'template')
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dest)

    cfg = workspace / 'game.toml'
    cfg.write_text(
        cfg.read_text(encoding='utf-8').replace(
            'disc = ""', 'disc = ' + json.dumps(str(disc))
        ),
        encoding='utf-8'
    )

    if not build:
        print('Preparacao de fontes concluida; nenhum dado de disco foi extraido.',
              flush=True)
        return workspace

    # Launcher: dependencia usada apenas no workspace pessoal de compilacao.
    ui = ensure_recomp_ui(workspace, env)
    cli = framework / 'psxrecomp_cli.py'

    run([sys.executable, cli, 'generate', '--project-root', workspace,
         '--config', cfg, '--disc', disc], workspace, env)

    # Ponto fundamental: a CLI gera PSX_RECOMP_UI OFF com CACHE ... FORCE.
    # Deve ser corrigido DEPOIS de generate e ANTES de rebuild.
    enable_launcher_in_generated_cmake(workspace)

    # Mantem ENHANCED e todas as demais configuracoes originais de build.
    run([sys.executable, cli, 'rebuild', '--project-root', workspace,
         '--config', cfg, '--build-dir', workspace / 'build',
         '--target', 'psx-runtime', '--exe-basename', 'BustAMove2JP_Pessoal',
         '--no-pgo',
         '--cmake-extra=-DPSX_EXECUTION_PROFILE=ENHANCED',
         '--cmake-extra=-DPSX_RECOMP_UI=ON',
         '--cmake-extra=-DRECOMP_UI_ROOT=' + str(ui)], workspace, env)

    check_launcher_cache(workspace)

    exe = workspace / 'build' / 'BustAMove2JP_Pessoal.exe'
    if not exe.is_file():
        raise RuntimeError('Build terminou sem o executavel esperado. Consulte o log.')

    (workspace / 'personal-install.json').write_text(
        json.dumps({'disc': str(disc), 'exe': str(exe),
                    'version': PIN['version']}, indent=2),
        encoding='utf-8'
    )
    print('Instalacao pessoal pronta, com launcher: ' + str(exe), flush=True)
    return workspace


def play(workspace):
    workspace = Path(workspace).resolve()
    info = json.loads((workspace / 'personal-install.json').read_text(encoding='utf-8'))
    exe = Path(info['exe']).resolve()
    if workspace not in exe.parents or not exe.is_file():
        raise RuntimeError('Instalacao pessoal invalida. Prepare novamente.')
    if not Path(info['disc']).is_file():
        raise RuntimeError('A imagem original selecionada nao esta disponivel.')

    saves = workspace / 'saves'
    saves.mkdir(exist_ok=True)

    # PRESERVAR: sao exatamente os ajustes de desempenho do prepare.py original.
    # Os valores sao passados tambem quando o launcher abre antes do jogo.
    env = {k: v for k, v in os.environ.items() if not k.startswith('PSX_')}
    env.update(
        PSX_FRAME_GEN='1',
        PSX_FRAME_GEN_METHOD='redraw',
        PSX_BAM2_POSE_FALLBACK='1',
        PSX_RENDER_THREAD='1',
        PSX_INTERNAL_RESOLUTION='native',
        PSX_DYNRES='0',
        PSX_BAM2_RP_SAFE='1',
        PSX_BAM2_RP_MAX_WARP_PX='1.25',
        PSX_FG_MAX_UNPLACED='0.10',
    )

    with (workspace / 'game-last-run.log').open('wb') as log:
        subprocess.Popen(
            [str(exe), '--launcher', '--game', str(workspace / 'game.toml'),
             '--renderer', 'opengl', '--memcard-dir', str(saves)],
            cwd=exe.parent,
            env=env,
            creationflags=subprocess.CREATE_NO_WINDOW,
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
        )
    print('Launcher iniciado com os ajustes de desempenho originais. '
          'Saves: ' + str(saves), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['prepare', 'play', 'sources'])
    parser.add_argument('--disc')
    parser.add_argument(
        '--workspace',
        default=str(Path(os.environ.get('LOCALAPPDATA', Path.home())) /
                    'BAM2RecompTest/v0.1')
    )
    parser.add_argument('--framework-cache', help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.action == 'play':
        play(args.workspace)
    else:
        if not args.disc:
            parser.error('--disc obrigatorio')
        prepare(args.disc, args.workspace, args.framework_cache,
                args.action == 'prepare')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('ERRO: ' + str(exc), file=sys.stderr, flush=True)
        sys.exit(1)

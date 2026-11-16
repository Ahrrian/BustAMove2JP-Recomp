"""Personal-disc builder. Never writes extracted or generated game data into the package."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

PACKAGE = Path(__file__).resolve().parents[1]
PIN = json.loads((PACKAGE/'framework.json').read_text())

def run(args, cwd, env):
    print('> ' + subprocess.list2cmdline([str(x) for x in args]), flush=True)
    subprocess.run([str(x) for x in args], cwd=cwd, env=env, check=True)

def prepare(disc, workspace, cache=None, build=True):
    if sys.version_info < (3, 11):
        raise RuntimeError('Instale Python 3.11 ou posterior.')
    if not shutil.which('git'):
        raise RuntimeError('Instale Git for Windows e reabra o assistente.')
    disc = Path(disc).resolve(strict=True)
    if disc.suffix.lower() != '.cue':
        raise ValueError('Selecione o .cue da edicao japonesa SLPM-86219, com os .bin correspondentes.')
    workspace = Path(workspace).resolve()
    if workspace == PACKAGE or PACKAGE in workspace.parents:
        raise ValueError('A instalacao pessoal deve ficar fora da pasta distribuivel.')
    workspace.mkdir(parents=True, exist_ok=True)
    env = {k:v for k,v in os.environ.items() if not k.startswith('PSX_')}
    env.update(CMAKE_BUILD_PARALLEL_LEVEL='2', PSXRECOMP_AOT_WORKERS='2', PYTHONUTF8='1', PYTHONUNBUFFERED='1')
    framework = workspace/'psxrecomp'
    if not framework.exists():
        run(['git','clone','--no-checkout',cache or PIN['repository'],framework],workspace,env)
        run(['git','checkout','--detach',PIN['commit']],framework,env)
        if cache:
            run(['git','remote','set-url','origin',PIN['repository']],framework,env)
    head = subprocess.check_output(['git','rev-parse','HEAD'],cwd=framework,text=True).strip()
    if head != PIN['commit']:
        raise RuntimeError('Framework em versao diferente; use outra pasta de instalacao pessoal.')
    # Only dependencies pinned by this checkout. No title repo/artwork downloads.
    run(['git','submodule','update','--init','--recursive'],framework,env)
    for p in (PACKAGE/'runtime-overrides').rglob('*'):
        if p.is_file():
            dest=framework/p.relative_to(PACKAGE/'runtime-overrides')
            dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
    for p in (PACKAGE/'template').rglob('*'):
        if p.is_file():
            dest=workspace/p.relative_to(PACKAGE/'template')
            dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
    cfg=workspace/'game.toml'
    cfg.write_text(cfg.read_text().replace('disc = ""','disc = '+json.dumps(str(disc))),encoding='utf-8')
    if not build:
        print('Preparacao de fontes concluida; nenhum dado de disco foi extraido.',flush=True)
        return workspace
    cli=framework/'psxrecomp_cli.py'
    run([sys.executable,cli,'generate','--project-root',workspace,'--config',cfg,'--disc',disc],workspace,env)
    run([sys.executable,cli,'rebuild','--project-root',workspace,'--config',cfg,
         '--build-dir',workspace/'build','--target','psx-runtime',
         '--exe-basename','BustAMove2JP_Pessoal','--no-pgo',
         '--cmake-extra=-DPSX_EXECUTION_PROFILE=ENHANCED'],workspace,env)
    exe=workspace/'build/BustAMove2JP_Pessoal.exe'
    if not exe.is_file():
        raise RuntimeError('Build terminou sem o executavel esperado. Consulte o log.')
    (workspace/'personal-install.json').write_text(json.dumps({'disc':str(disc),'exe':str(exe),'version':PIN['version']},indent=2))
    print('Instalacao pessoal pronta: '+str(exe),flush=True)
    return workspace

def play(workspace):
    workspace=Path(workspace).resolve()
    info=json.loads((workspace/'personal-install.json').read_text())
    exe=Path(info['exe']).resolve()
    if workspace not in exe.parents or not exe.is_file():
        raise RuntimeError('Instalacao pessoal invalida. Prepare novamente.')
    if not Path(info['disc']).is_file():
        raise RuntimeError('A imagem original selecionada nao esta disponivel.')
    saves=workspace/'saves';saves.mkdir(exist_ok=True)
    env={k:v for k,v in os.environ.items() if not k.startswith('PSX_')}
    env.update(PSX_FRAME_GEN='1',PSX_FRAME_GEN_METHOD='redraw',PSX_BAM2_POSE_FALLBACK='1',
               PSX_RENDER_THREAD='1',PSX_INTERNAL_RESOLUTION='native',PSX_DYNRES='0',
               PSX_BAM2_RP_SAFE='1',PSX_BAM2_RP_MAX_WARP_PX='1.25',PSX_FG_MAX_UNPLACED='0.10')
    with (workspace/'game-last-run.log').open('wb') as log:
        subprocess.Popen([str(exe),'--no-launcher','--renderer','opengl','--memcard-dir',str(saves)],
                         cwd=exe.parent,env=env,creationflags=subprocess.CREATE_NO_WINDOW,
                         stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT)
    print('Jogo iniciado. Saves: '+str(saves),flush=True)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('action',choices=['prepare','play','sources'])
    parser.add_argument('--disc')
    parser.add_argument('--workspace',default=str(Path(os.environ.get('LOCALAPPDATA',Path.home()))/'BAM2RecompTest/v0.1'))
    parser.add_argument('--framework-cache',help=argparse.SUPPRESS)
    args=parser.parse_args()
    if args.action=='play':play(args.workspace)
    else:
        if not args.disc:parser.error('--disc obrigatorio')
        prepare(args.disc,args.workspace,args.framework_cache,args.action=='prepare')

if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('ERRO: '+str(exc),file=sys.stderr,flush=True);sys.exit(1)

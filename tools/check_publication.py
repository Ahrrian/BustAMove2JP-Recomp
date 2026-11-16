#!/usr/bin/env python3
"""Fail-closed review of the GitHub source-only package (no user disc required).

Usage: python tools/check_publication.py [--root PATH] [--tracked]

Checks a curated set of public paths, checksums and obvious forbidden content.
It cannot prove copyright ownership, security, or legal permission to publish.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

EXPECTED_ROOT = {
    ".gitignore", ".gitattributes", "README.md", "LEIA-ME.txt",
    "VALIDACAO.txt", "RELEASE_CHECKLIST.md", "framework.json",
    "manifest-sha256.json",
}
EXPECTED_FILES = EXPECTED_ROOT | {
    "licenses/NOTICE.txt", "licenses/assistant-MIT.txt", "licenses/psxrecomp-LICENSE.txt",
    "licenses/xBR-Hyllian-MIT.txt",
    "source/Assistente.cs", "source/prepare.py", "source/build-assistant.cmd",
    "template/CMakeLists.txt", "template/game.toml", "template/seeds/ghidra_funcs.txt",
    "runtime-overrides/runtime/include/frame_gen.h",
    "runtime-overrides/runtime/include/gpu_gl_renderer.h",
    "runtime-overrides/runtime/src/frame_gen.c",
    "runtime-overrides/runtime/src/gpu_gl_renderer.c",
    "runtime-overrides/runtime/src/main.cpp",
    "runtime-overrides/runtime/src/render_thread.c",
    "runtime-overrides/runtime/src/savestate.c",
    "runtime-overrides/runtime/tests/test_frame_gen.c",
    "tools/check_publication.py", ".github/workflows/publication-check.yml",
}
FORBIDDEN_SUFFIXES = {
    ".exe", ".dll", ".iso", ".bin", ".cue", ".img", ".chd", ".pbp",
    ".sbi", ".mdf", ".mds", ".ccd", ".wav", ".xa", ".str", ".tim",
    ".vag", ".mp3", ".ogg", ".flac", ".mp4", ".avi", ".mkv", ".webp",
    ".png", ".jpg", ".jpeg", ".bmp", ".gif", ".zip", ".7z",
    ".a", ".o", ".obj", ".lib", ".pdb", ".ranges", ".elf",
    ".mcr", ".mcd", ".sav", ".sst", ".dmp", ".dump", ".state",
}
SECRETS = [
    re.compile(rb"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(rb"\bgh[pousr]_[A-Za-z0-9_]{30,}\b"),
    re.compile(rb"\bgithub_pat_[A-Za-z0-9_]{50,}\b"),
    re.compile(rb"\bAKIA[0-9A-Z]{16}\b"),
]
BAD_DIR = {"generated", "build", "disco", "disc", "cache", ".cache", ".vs", "saves", "_private"}


def check(root: Path, tracked: bool = False) -> list[str]:
    errors: list[str] = []
    if not root.is_dir():
        return [f"Pasta inexistente: {root}"]
    physical = {}
    for p in root.rglob("*"):
        rel = p.relative_to(root)
        if ".git" in rel.parts or "__pycache__" in rel.parts:
            continue  # .git metadata is never itself staged as a regular file
        name = rel.as_posix()
        if p.is_symlink():
            errors.append(f"Link simbólico proibido: {name}")
        elif p.is_file():
            physical[name] = p
        elif p.is_dir() and p.name.casefold() in BAD_DIR:
            errors.append(f"Pasta reservada ou sensível: {name}")
    unknown = sorted(set(physical) - EXPECTED_FILES)
    missing = sorted(EXPECTED_FILES - set(physical))
    errors.extend(f"Arquivo não autorizado (bloqueado): {p}" for p in unknown)
    errors.extend(f"Arquivo obrigatório ausente: {p}" for p in missing)

    for name,p in physical.items():
        if p.suffix.lower() in FORBIDDEN_SUFFIXES or p.name.lower() in {"overlay_captures.json", "personal-install.json"}:
            errors.append(f"Tipo não publicável: {name}")
        if p.stat().st_size > 3_000_000:
            errors.append(f"Arquivo grande demais (> 3 MB): {name}")
        raw = p.read_bytes()
        if raw[:2] == b"MZ" or raw[:8] == b"\x7fELF" or raw[:4] in {b"RIFF", b"OggS", b"PK\x03\x04"}:
            errors.append(f"Cabeçalho binário inesperado: {name}")
        if any(pattern.search(raw) for pattern in SECRETS):
            errors.append(f"Padrão de credencial presente: {name}")
        try:
            raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            errors.append(f"Arquivo não é texto UTF-8: {name}")
    try:
        data = json.loads((root / "manifest-sha256.json").read_text(encoding="utf-8-sig"))
        expected_manifest = set(physical) - {"manifest-sha256.json"}
        if set(data) != expected_manifest:
            errors.append("Inventário diferente dos arquivos reais: " +
                          f"faltam={sorted(expected_manifest-set(data))}; " +
                          f"excedem={sorted(set(data)-expected_manifest)}")
        for name in set(data) & set(physical):
            body = physical[name].read_bytes()
            if data[name].get("bytes") != len(body) or data[name].get("sha256") != hashlib.sha256(body).hexdigest():
                errors.append(f"SHA-256 ou tamanho diferente do manifesto: {name}")
    except (OSError, json.JSONDecodeError, TypeError, AttributeError, KeyError) as exc:
        errors.append(f"Manifesto inválido: {exc}")
    try:
        seed_lines = (root/"template/seeds/ghidra_funcs.txt").read_text(encoding="utf-8").splitlines()
        seeds = [line.strip() for line in seed_lines if line.strip() and not line.startswith("#")]
        if len(seeds) != 588:
            errors.append(f"A lista de seeds não contém 588 entradas: {len(seeds)}")
        for i,seed in enumerate(seeds):
            if not re.fullmatch(r"(?:0x)?[0-9a-fA-F]{8}", seed):
                errors.append(f"Seed com conteúdo não numérico na linha {i+1}: {seed[:60]}")
                break
    except OSError as exc:
        errors.append(f"Falha ao ler seeds: {exc}")

    if tracked:
        result = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], capture_output=True)
        if result.returncode != 0:
            errors.append("Não foi possível verificar os caminhos rastreados pelo Git")
        else:
            tracked_paths = {name.decode("utf-8") for name in result.stdout.split(b"\x00") if name}
            for name in sorted(tracked_paths - EXPECTED_FILES):
                errors.append(f"Arquivo rastreado pelo Git não autorizado: {name}")
            if not tracked_paths:
                errors.append("Nenhum arquivo rastreado: rode git add apenas depois da auditoria")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    ap.add_argument("--tracked", action="store_true", help="Valida também arquivos já registrados no Git")
    opts = ap.parse_args()
    root = opts.root.resolve()
    errors = check(root, opts.tracked)
    if errors:
        print(f"BLOQUEADO: {len(errors)} problema(s) na pasta pública {root}")
        for e in errors:
            print("  -", e)
        return 1
    print(f"OK: {len(EXPECTED_FILES)} arquivos públicos verificados; sem arquivos adicionais; SHA-256 consistente.")
    print("Aviso: verificação automática NÃO substitui revisão jurídica/autoral nem teste Windows limpo.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

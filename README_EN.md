# Bust A Move 2 JP — Native Recompilation

[**Português (Brasil)**](README.md) | **English**

**Experimental native-recompilation project for Windows**  
**Version:** v0.1 (source code) · **Status:** in development (experimental) · **Maintainer:** Ahrian · **Platform:** Windows · **Target game:** *Bust A Move 2: Dance Tengoku Mix* (Japanese PlayStation release, SLPM-86219)

> **This repository does not include the game.** It distributes only tools, configuration files, and modifications to [PSXRecomp](https://github.com/RetroPortingToolKit/psxrecomp). Users must lawfully obtain their own compatible files from the original game disc and generate their builds **locally**.

**Disclaimer:** This is an unofficial community development and research project. **No game files, disc images, commercial assets, original game executable, generated game code, or precompiled game binaries are distributed.**

---

## Contents

- [About the project](#about-the-project)
- [What's included in v0.1](#whats-included-in-v01)
- [Requirements and compatibility](#requirements-and-compatibility)
- [Installation and first launch](#installation-and-first-launch)
- [Where personal files are stored](#where-personal-files-are-stored)
- [Repository structure](#repository-structure)
- [Current status and limitations](#current-status-and-limitations)
- [Roadmap](#roadmap)
- [Troubleshooting](#troubleshooting)
- [Package integrity and publication checks](#package-integrity-and-publication-checks)
- [Licenses and credits](#licenses-and-credits)
- [Contributing](#contributing)

## About the project

This project explores **native recompilation of an original PlayStation game for Windows**, using the PSXRecomp framework. The work focuses on integrating locally generated code with a modern runtime, OpenGL rendering, and experimental frame-presentation techniques.

The priority is to preserve the game's behavior—particularly **music, rhythm, and input judgment timing**—while researching visual improvements and compatibility. This is an **unofficial, noncommercial community project**, and development is ongoing.

This project **is not a remake**, does not replace a legitimate copy of the game, and does not offer downloads of commercial game content.

> 🚧 **Work in progress:** v0.1 is an early experimental release. **User-selectable presentation rates up to a target of 360 FPS and online play using rollback netcode are future goals. Neither feature is available or guaranteed in v0.1.** See the [roadmap](#roadmap).

## What's included in v0.1

| Component | Status in v0.1 |
| --- | --- |
| Windows graphical assistant | C# source code included; compile locally |
| Command-line setup | Python script included |
| Framework download | Automated and pinned to a specific commit |
| Japanese game configuration | Included for **SLPM-86219** |
| Modified runtime code | Included under `runtime-overrides/` |
| Rendering | Runtime configured for **OpenGL** |
| Frame generation | **Experimental**; the default launch mode is `redraw` |
| Reprojection and visual safeguards | Experimental code included, **not enabled as the default launch mode** |
| User-selectable presentation rate (up to 360 FPS) | **Planned; not yet available** |
| Online multiplayer with rollback netcode | **Planned; not yet available** |
| Game, commercial BIOS, or ready-to-run game executable | **Not included** |

**Important:** A monitor's refresh rate, the original game's simulation rate, and the number of generated intermediate frames are different things. There is no promise of **360 unique game frames per second**, artifact-free visuals, or guaranteed lower input latency.

## Requirements and compatibility

- **64-bit Windows**.
- **Python 3.11 or later**, available as `py -3` or `python`.
- **Git for Windows** and internet access to obtain PSXRecomp and its submodules.
- The development tools and dependencies required by **PSXRecomp**, including the appropriate Windows C/C++ toolchain and CMake.
- Enough available disk space for dependencies, generated code, and the local build.
- A **`.cue` file from the Japanese SLPM-86219 release**, together with the `.bin` files it references, lawfully obtained by the user.
- To compile the **graphical assistant**, the **.NET Framework 4.x** C# compiler (`csc.exe`) at the path used by `source/build-assistant.cmd`.

The supplied configuration targets this specific Japanese edition. **Other regions, editions, and disc revisions are not claimed to be compatible.** The preparation process uses layout information and identifiers specific to the target edition.

## Installation and first launch

### Option A — Python command line (recommended for troubleshooting)

**1.** Download this repository's source code and extract it to a folder of your choice. Do not place game files inside the repository folder.

**2.** Check that Python and Git are available in PowerShell:

```powershell
py -3 --version
git --version
```

**3.** Open PowerShell in the repository folder and run the setup command. Replace the example with the **actual path** to your `.cue` file:

```powershell
py -3 .\source\prepare.py prepare --disc 'D:\MyGames\BAM2JP.cue'
```

The setup downloads PSXRecomp at the pinned commit, initializes its submodules, applies this project's runtime modifications, then attempts to generate and compile a **personal, local** version of the game. The initial run requires an internet connection and may require installing additional build-toolchain components.

**4.** After setup completes successfully, launch the personal build:

```powershell
py -3 .\source\prepare.py play
```

If compilation fails, save the error message and consult [Troubleshooting](#troubleshooting). Do not redistribute temporary files or generated game content.

### Option B — Windows graphical assistant

This repository provides the assistant's **source code**, not a prebuilt `Assistente_BAM2.exe`.

**1.** From the repository folder, run:

```cmd
source\build-assistant.cmd
```

**2.** If the C# compiler is available, this creates `Assistente_BAM2.exe` locally in the project root.

**3.** Open the assistant, select your `.cue` file, read the notices, and confirm that you have an appropriate copy of the game. Select **“1. Preparar minha cópia”** (*Prepare my copy*).

**4.** Once that operation finishes successfully, select **“2. Jogar”** (*Play*).

The assistant invokes the same Python script used by Option A. It does not rip physical discs or download the game. **The assistant's interface is currently in Portuguese.**

## Where personal files are stored

By default, the preparation script uses:

```text
%LOCALAPPDATA%\BAM2RecompTest\v0.1
```

This directory holds the downloaded framework, locally generated files based on your disc, your personal build, saves, and logs. Your original disc files remain at the location you selected.

**Do not upload this directory to GitHub or share your personal executable, extracted data, saves, caches, or generated game code.** The public repository includes only the files described below.

## Repository structure

```text
.
├── README.md                         # Portuguese documentation (default)
├── README_EN.md                      # English documentation
├── LEIA-ME.txt                       # Short instructions (Portuguese)
├── RELEASE_CHECKLIST.md              # Publication checklist
├── VALIDACAO.txt                     # Historical testing notes and limitations
├── framework.json                    # PSXRecomp repository and pinned commit
├── manifest-sha256.json              # Integrity data for public files
├── source/
│   ├── Assistente.cs                  # Windows UI (C#)
│   ├── build-assistant.cmd            # Local assistant build script
│   └── prepare.py                     # Local setup / personal game build
├── template/
│   ├── game.toml                      # SLPM-86219 configuration
│   ├── CMakeLists.txt                 # CMake configuration
│   └── seeds/ghidra_funcs.txt         # Numerical function addresses
├── runtime-overrides/                # Modified PSXRecomp source files
├── licenses/                         # Licenses and attribution notices
├── tools/check_publication.py        # Prepublication integrity audit
└── .github/workflows/                 # Automated publication audit
```

`template/seeds/ghidra_funcs.txt` contains **588 numerical addresses** obtained during technical analysis of the original executable; it does not contain MIPS instructions. This metadata does not replace the game, but its use and redistribution may still be subject to applicable laws.

## Current status and limitations

**v0.1 is experimental.** Its purpose is to provide a reproducible foundation for development and research, rather than to announce a finished PC port.

- The default launch configuration in `source/prepare.py` uses `PSX_FRAME_GEN_METHOD=redraw`. **Reprojection** is still experimental and may produce visual artifacts.
- Actual frame presentation depends on the game, hardware, renderer, and settings. A 360 Hz display does not imply 360 unique frames per second. **User-selected FPS targets are on the roadmap; they are not a v0.1 feature.**
- Compatibility is not guaranteed across all Windows versions, GPUs, or systems.
- [`VALIDACAO.txt`](VALIDACAO.txt) documents historical development tests; **a complete installation from the public source-only package has not yet been independently verified on a clean Windows system**.
- Complete validation across every song, musical synchronization scenario, and input judgment situation has not been claimed.
- **v0.1 does not provide functional online multiplayer or rollback netcode.**
- The local build depends on PSXRecomp, its licenses, and dependencies downloaded during setup.

For release readiness, consult [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md).

## Roadmap

The following items are **development goals, not completed features or committed release dates**. Priorities may change based on testing results, technical constraints, and community contributions.

| Stage | Goal | Status |
| --- | --- | --- |
| 1. Native Windows foundation | Consolidate local builds, the assistant, and compatibility with the Japanese SLPM-86219 edition | **Experimental foundation in v0.1** |
| 2. Quality and stability | Investigate visual regressions, renderer improvements, audio, music synchronization, and input response | **In development** |
| 3. Configurable presentation rate | Let users choose a presentation target, with options up to **360 FPS** on suitable hardware, using frame generation where needed | **Planned** |
| 4. Online multiplayer | Investigate online matches using **rollback netcode**, input prediction, snapshots, and resimulation | **Planned / long-term research** |

### Presentation-rate goal: up to 360 FPS

The intention is to explore user-selectable settings such as **30, 60, 120, 144, 165, 240, and 360 FPS**, wherever technically feasible. These are **future visual presentation targets**, not achieved or certified results. The goal is to improve perceived smoothness **without speeding up the music, core game simulation, or timing windows for input judgments**. The original simulation rate and presentation of additional frames must remain separate.

Even if implemented, the effective presentation rate will depend on GPU, CPU, drivers, display capabilities, and scene complexity. Frame generation can introduce artifacts or latency, and its quality and stability will need to be demonstrated before advertising definitive 360 FPS support.

### Online multiplayer with rollback netcode

A long-term goal is to enable **online play between players** using rollback netcode. This requires investigation into deterministic simulation, synchronization of inputs and music, rapid state capture and restoration, remote input prediction, and safe resimulation under real-world network latency.

**Rollback netcode is not the same as the experimental visual defect where an earlier frame or pose briefly reappears during reprojection.** They are unrelated issues. **v0.1 has no online-match infrastructure or rollback netcode.**

No release dates have been announced for these goals. Community feedback and technical testing may influence the roadmap.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| `py` or `python` not found | Install Python 3.11+ and verify your PATH |
| `git` not found | Install Git for Windows and reopen your terminal |
| `.cue` rejected | Check the **SLPM-86219** Japanese edition, referenced `.bin` files, and the selected path |
| `generate` or `rebuild` fails | Check PSXRecomp's required toolchain, dependencies, and the full PowerShell output |
| `csc.exe` not found | Install the required .NET Framework 4.x components, or use the Python setup method |
| `play` fails | Successfully run `prepare` first; do not delete the personal installation directory |
| Visual artifacts or inconsistent performance | Frame generation is experimental; record the circumstances and diagnostic messages before filing a report |

When reporting a bug, include your Windows version, GPU, the stage where the issue occurred, and **relevant diagnostic messages**, with personal paths, emails, disc data, and private information removed. Do not attach the game or content extracted from it.

## Package integrity and publication checks

Before committing distribution changes, run this **from the repository folder**:

```powershell
py -3 .\tools\check_publication.py
```

The checker uses an explicit list of permitted files, verifies **file sizes and SHA-256 hashes** against `manifest-sha256.json`, and rejects disallowed file types and directories. The GitHub Actions workflow also checks tracked files in commits.

**Note:** whenever a public file changes, its manifest entry must be updated deliberately before committing. Automated checks do not prove authorship, license compliance, source-code security, or the absolute absence of copyrighted material.

## Licenses and credits

**There is no single repository-wide license covering every component.** Review each component's notices before reuse.

| Component | Origin / license |
| --- | --- |
| Project-owned assistant, scripts, and documentation covered by the notices | **MIT**, credited publicly to **Ahrian**, subject to the scope in [`licenses/assistant-MIT.txt`](licenses/assistant-MIT.txt) and [`licenses/NOTICE.txt`](licenses/NOTICE.txt) |
| Modified PSXRecomp source files under `runtime-overrides/` | **PolyForm Noncommercial 1.0.0** and applicable additional notices; **not relicensed under MIT** |
| xBR algorithm/filter adapted in the renderer | Work attributed to **Hyllian**, licensed under MIT; see [`licenses/xBR-Hyllian-MIT.txt`](licenses/xBR-Hyllian-MIT.txt) |
| Game, trademarks, music, characters, and commercial assets | Rights remain with their respective owners; **not distributed or licensed by this project** |

**Credits:**

- **Ahrian** — project maintainer and public adaptation; assistant and documentation developed with assistance from **OpenAI Codex/ChatGPT**.
- **Matthew Stanley and PSXRecomp contributors** — recompilation framework and runtime. [Upstream repository](https://github.com/RetroPortingToolKit/psxrecomp), [pinned commit](https://github.com/RetroPortingToolKit/psxrecomp/tree/b263b8552e5b8838b317f8921dfde8b6aca97904), [additional permissions](https://github.com/RetroPortingToolKit/psxrecomp/blob/b263b8552e5b8838b317f8921dfde8b6aca97904/PERMISSIONS.md), and [third-party attributions](https://github.com/RetroPortingToolKit/psxrecomp/blob/b263b8552e5b8838b317f8921dfde8b6aca97904/THIRD_PARTY_ATTRIBUTION.md).
- **Hyllian** — original xBR algorithm work, with license and attribution notices preserved.

References to commercial names identify the target game only. **This project is not affiliated with, authorized by, or endorsed by the rights holders of *Bust A Move 2* or its trademarks.** Rights to copy, extract, or use game content vary by jurisdiction and are not granted by this repository.

## Contributing

Technical reports, documentation fixes, and suggestions are welcome through GitHub's collaboration features when enabled. Before submitting changes:

1. Do not include ROMs, ISOs, BIN/CUE, commercial BIOS files, assets, memory dumps, generated game code, or recompiled game executables.
2. Respect each component's license and preserve third-party notices.
3. Review `RELEASE_CHECKLIST.md` and run `py -3 .\tools\check_publication.py`.
4. Describe your testing environment and avoid claims about features or performance that have not been verified.

---

**Experimental, noncommercial, unofficial project.** Thank you for supporting responsible technical research, game preservation, and development.

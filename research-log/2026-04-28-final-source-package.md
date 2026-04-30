# 2026-04-28 Final Source Package

Repository: `D:\Codex\skillops-paper-artifact-benchmark`
Branch: `paper-source-package`
Base commit: `f28604b071d9eb628034603dedb6eafd01daef74`

## Commands Run

```powershell
git status -sb
git rev-parse HEAD
git rev-parse origin/main
git config user.name
git config user.email
git checkout -b paper-source-package
& 'C:\Users\luosong03\AppData\Local\Programs\Python\Python311\python.exe' scripts\run_all.py
& 'C:\Users\luosong03\AppData\Local\Programs\Python\Python311\python.exe' scripts\run_tests.py
```

Packaging commands:

```powershell
if (Test-Path 'release\skillops-preprint-source') { Remove-Item -LiteralPath 'release\skillops-preprint-source' -Recurse -Force }
if (Test-Path 'release\skillops-preprint-source.zip') { Remove-Item -LiteralPath 'release\skillops-preprint-source.zip' -Force }
New-Item -ItemType Directory -Path 'release\skillops-paper-source' -Force | Out-Null
Copy-Item -LiteralPath 'paper\main.tex' -Destination 'release\skillops-paper-source\main.tex' -Force
Copy-Item -LiteralPath 'paper\references.bib' -Destination 'release\skillops-paper-source\references.bib' -Force
Compress-Archive -LiteralPath 'release\skillops-paper-source' -DestinationPath 'release\skillops-paper-source.zip' -Force
```

## Package Contents

- `release/skillops-paper-source/main.tex`
- `release/skillops-paper-source/references.bib`
- `release/skillops-paper-source/README.md`
- `release/skillops-paper-source.zip`

## Notes

- The source package intentionally excludes external SVG figure assets because `paper/main.tex` uses LaTeX-native figures.
- Textual references to omitted `.svg` asset paths were removed from figure captions before the packaged `main.tex` copy was refreshed.
- Static checks are limited to source inspection because no local LaTeX compiler is available in this environment.
- `scripts\run_tests.py` was rerun after the caption cleanup and still passed `22/22`.
- Static package audit passed for file existence, citation coverage, label coverage, author metadata, absence of direct SVG inclusion, absence of missing external figure paths, absence of prohibited public-facing wording, and absence of unsupported affirmative claim wording.

# ZAI Coder Install Guide

## Overview
Safe local installation for ZAI Coder Control Plane.

## Prerequisites
- Bash, Python 3.10+, make
- Git (configured)

## Installation

### Dry-run (Preview)
```bash
make install-dry-run
```

### Real Install
```bash
make install APPLY=1
```
*(Default prefix: ~/.local/share/zai-coder)*

### Custom Path
```bash
PREFIX=/custom/path make install APPLY=1
```

## Post-Install
```bash
make post-install-check
~/.local/bin/zai-coder doctor
```

## Uninstall
```bash
make uninstall APPLY=1
```
EOF

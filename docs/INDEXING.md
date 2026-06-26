# Local Source Indexing

ZAI Coder implements a local, SQLite-based source code indexing system for fast project navigation, context retrieval, and symbol tracking.

## Architecture

The indexing system avoids remote databases or heavyweight engines. It uses the Python standard library `sqlite3` to maintain state locally within `.zai-coder/index/project-index.db`.

### Database Schema

- `files`: Tracks unique file paths, sizes, language, and SHA-256 hashes to prevent redundant parsing.
- `chunks`: Stores 50-line blocks of code with associated hashes to allow semantic or text-based search.
- `symbols`: Stores extracted classes and functions with their line numbers.

### Language Detection & Parsing
- Detects Python, JavaScript, TypeScript, React, Shell, and Compiled languages using file extensions.
- Extracts standard definitions (`class`, `def`, `export function`) into the `symbols` table for rapid lookups.

## Usage

```bash
# Build or update the index
./zai-coder index build

# Search for a symbol or keyword
./zai-coder index search "SafetyPolicy"

# View index metrics
./zai-coder index stats

# Clear the index completely
./zai-coder index clear --apply
```

## Ignored Paths

The indexer automatically ignores:
- Repositories (`.git`)
- Virtual environments (`.venv`, `venv`)
- Caches (`__pycache__`, `.pytest_cache`)
- Node modules (`node_modules`)
- Build outputs (`dist`, `build`, `.next`, `out`)
- Binary and archive formats
- Secret files (`.env`, `.key`, `token`)

Secrets are explicitly redacted using `redact_text` prior to hashing or insertion.

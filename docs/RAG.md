# Local RAG Retrieval

ZAI Coder implements Local Retrieval-Augmented Generation (RAG) to provide automated context for prompt execution (`ask` and `plan`) directly from the local project workspace.

## Architecture

1. **Indexer**: Relies on the `ProjectIndexer` mapping project content to SQLite chunks.
2. **Retrieval**: Leverages lexical analysis across chunks and symbols to score hits.
3. **Redaction**: All chunks and context blocks pass through regex-based redactors to strip secrets before injecting into the language model.

## Redaction Capabilities

The system ensures security by stripping the following before sending any codebase context to models:
- OpenAI & OpenRouter API Keys (`sk-...`)
- AWS API Keys (`AKIA...`)
- GitHub Tokens (`ghp_...`)
- Google API Keys (`AIza...`)
- Private Keys (RSA, EC, OPENSSH)
- Bearer Tokens
- JSON/YAML/TOML strings mapped to `password`, `secret`, `token`, `api_key`
- `.env` assignment blocks

## Usage

```bash
# Force build or refresh the index
./zai-coder rag build

# Query RAG to observe exact returned context and chunks
./zai-coder rag query "where is command safety enforced"

# Inject RAG context automatically into an 'ask' query
./zai-coder ask "review safety policy" --with-rag

# Inject RAG context automatically into a 'plan'
./zai-coder plan --task "upgrade server" --with-rag
```

## Boundaries
- No external Vector Database required.
- Context injection restricts chunk limit logically to avoid exceeding model context limits.
- Bounded token lengths in the orchestrator prevent runaway loops.

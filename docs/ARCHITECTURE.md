# Architecture
ZAI Coder operates in a local-first offline manner.
The core engine interacts with:
- **Index Engine**: SQLite-backed schema.
- **Patcher Runtime**: Unifed diff applicators.
- **Command Engine**: Secure subprocess routers tracking against `.zai-coder/config.json` boundaries.
- **Monitoring**: Native system-hook reads polling environment states without blocking events.

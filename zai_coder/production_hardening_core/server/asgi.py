"""ASGI entrypoint.

Run after installing production requirements:

```bash
uvicorn zai_coder.production_hardening_core.server.asgi:app --host 127.0.0.1 --port 8765
```
"""

from __future__ import annotations

from .app_factory import create_app

app = create_app()

from __future__ import annotations

def render_release_notes(version: str = "v0.12.0") -> str:
    return f"""# ZAI Coder Control Plane {version}

## Highlights

- Local-first AI coding control plane.
- Final App Studio shell.
- Production SaaS scaffold.
- Deployment and integration planning.
- GitHub-ready release package.

## Validation

```bash
python3 -m pytest -q
make repo-check
make secret-scan
make stage-manifest-check
```
"""

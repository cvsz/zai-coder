from __future__ import annotations

import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .agents.registry import build_agent
from .cli import _ask, build_audit, build_memory
from .core.project import scan_project
from .core.registry import JsonRegistry

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"


def run_server(cfg, host: str = "127.0.0.1", port: int = 8765) -> int:
    web_root = (ROOT / cfg.web_root).resolve()

    class Handler(BaseHTTPRequestHandler):
        server_version = "ZaiCoderHTTP/1.0"

        def log_message(self, fmt, *args):  # noqa: ANN001
            build_audit(cfg).write("http.access", True, fmt % args, path=self.path)

        def send_json(self, data, status=200):
            body = json.dumps(data, ensure_ascii=False, default=str).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def read_json(self):
            length = int(self.headers.get("Content-Length", "0") or "0")
            if length > 2_000_000:
                raise ValueError("Request too large")
            raw = self.rfile.read(length).decode("utf-8") if length else "{}"
            return json.loads(raw or "{}")

        def do_GET(self):  # noqa: N802
            parsed = urlparse(self.path)
            if parsed.path == "/api/health":
                return self.send_json({"ok": True, "model": cfg.model, "provider": cfg.provider})
            if parsed.path == "/api/agents":
                return self.send_json([i.__dict__ for i in JsonRegistry(ASSETS / "agents").list()])
            if parsed.path == "/api/skills":
                return self.send_json([i.__dict__ for i in JsonRegistry(ASSETS / "skills").list()])
            if parsed.path == "/api/memory":
                q = parse_qs(parsed.query)
                namespace = q.get("namespace", ["project"])[0]
                return self.send_json([i.__dict__ for i in build_memory(cfg).list(namespace, 100)])
            if parsed.path == "/api/runs":
                return self.send_json(build_memory(cfg).recent_runs(50))
            if parsed.path == "/api/audit":
                return self.send_json(build_audit(cfg).tail(100))
            if parsed.path == "/api/scan":
                return self.send_json(scan_project(cfg.workspace).__dict__)
            return self.serve_static(parsed.path, web_root)

        def do_POST(self):  # noqa: N802
            try:
                data = self.read_json()
                if self.path == "/api/ask":
                    prompt = str(data.get("prompt", ""))[:50_000]
                    agent = str(data.get("agent", "coder"))
                    res = _ask(cfg, prompt, agent)
                    return self.send_json({"ok": res.ok, "content": res.content, "model": res.model, "provider": res.provider, "error": res.error})
                if self.path == "/api/memory":
                    build_memory(cfg).set(str(data["key"]), str(data["value"]), str(data.get("namespace", "project")))
                    return self.send_json({"ok": True})
                return self.send_json({"ok": False, "error": "not found"}, 404)
            except Exception as exc:  # noqa: BLE001
                build_audit(cfg).write("http.error", False, str(exc), path=self.path)
                return self.send_json({"ok": False, "error": str(exc)}, 500)

        def serve_static(self, request_path: str, web_root: Path):
            rel = request_path.lstrip("/") or "index.html"
            target = (web_root / rel).resolve()
            if not str(target).startswith(str(web_root)) or not target.exists() or target.is_dir():
                target = web_root / "index.html"
            body = target.read_bytes()
            ctype = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    httpd = ThreadingHTTPServer((host, port), Handler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        return 0
    finally:
        httpd.server_close()
    return 0

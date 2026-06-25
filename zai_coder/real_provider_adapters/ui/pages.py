from __future__ import annotations
from html import escape
from zai_coder.real_provider_adapters.registry import list_provider_actions

def render_provider_shell(title: str, body: str) -> str:
    return f'''<!doctype html><html><head><meta charset="utf-8"><title>{escape(title)}</title><style>body{{font-family:system-ui;background:#020617;color:#e2e8f0;margin:0}}nav{{background:#0f172a;padding:16px;display:flex;gap:14px}}a{{color:#7dd3fc;text-decoration:none}}main{{padding:24px}}table{{width:100%;border-collapse:collapse}}td,th{{border:1px solid #334155;padding:8px}}</style></head><body><nav><a href="/providers">Providers</a><a href="/providers/audit">Audit</a></nav><main>{body}</main></body></html>'''

def render_providers_page() -> str:
    rows = '\n'.join(f"<tr><td>{escape(item['provider'])}</td><td>{escape(item['action'])}</td><td>{item['mutating']}</td></tr>" for item in list_provider_actions())
    return render_provider_shell('Provider Adapters', f'<h1>Real Provider Adapters</h1><table><tbody>{rows}</tbody></table>')

def render_provider_audit_page(events: list[dict]) -> str:
    rows = '\n'.join(f"<tr><td>{escape(e.get('provider',''))}</td><td>{escape(e.get('action',''))}</td><td>{escape(e.get('actor',''))}</td><td>{e.get('dry_run')}</td><td>{e.get('ok')}</td></tr>" for e in events)
    return render_provider_shell('Provider Audit', f'<h1>Provider Audit</h1><table><tbody>{rows}</tbody></table>')

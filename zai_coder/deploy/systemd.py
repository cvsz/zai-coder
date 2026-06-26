def get_systemd_template(app_name: str = "zai-coder") -> str:
    return f"""[Unit]
Description={app_name} local service
After=network.target

[Service]
Type=simple
User=appuser
WorkingDirectory=/opt/{app_name}
ExecStart=/opt/{app_name}/venv/bin/python -m {app_name.replace('-', '_')} serve --host 127.0.0.1 --port 8765
Restart=on-failure
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
"""

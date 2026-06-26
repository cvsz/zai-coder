def get_nginx_template(app_name: str = "zai-coder") -> str:
    return f"""server {{
    listen 127.0.0.1:80;
    server_name localhost;

    location / {{
        proxy_pass http://127.0.0.1:8765;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}
"""

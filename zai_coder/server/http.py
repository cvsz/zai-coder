import json
from http.server import BaseHTTPRequestHandler

MAX_REQUEST_SIZE = 1024 * 1024 # 1MB limit

class JsonHTTPRequestHandler(BaseHTTPRequestHandler):
    def send_json_response(self, status_code: int, data: dict):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json_body(self):
        content_length_str = self.headers.get("Content-Length")
        if not content_length_str:
            return {}
        try:
            content_length = int(content_length_str)
        except ValueError:
            return None
        if content_length > MAX_REQUEST_SIZE:
            self.send_json_response(413, {"error": "Payload too large"})
            return None
        
        body_bytes = self.rfile.read(content_length)
        try:
            return json.loads(body_bytes.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self.send_json_response(400, {"error": "Invalid JSON"})
            return None

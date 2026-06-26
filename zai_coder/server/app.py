from http.server import HTTPServer
from urllib.parse import urlparse
from zai_coder.server.http import JsonHTTPRequestHandler
from zai_coder.server.routes import handle_get, handle_post

class ZaiServerHandler(JsonHTTPRequestHandler):
    config_path = None
    
    def do_GET(self):
        parsed = urlparse(self.path)
        handle_get(self, parsed.path)
        
    def do_POST(self):
        parsed = urlparse(self.path)
        body = self.read_json_body()
        if body is None:
            return # read_json_body handles the error response
        handle_post(self, parsed.path, body, self.config_path)

def run_server(host: str, port: int, config_path: str = None):
    ZaiServerHandler.config_path = config_path
    server = HTTPServer((host, port), ZaiServerHandler)
    server.serve_forever()

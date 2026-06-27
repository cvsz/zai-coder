import pytest
from unittest.mock import MagicMock
from zai_coder.server.routes import handle_get
import zai_coder

def test_server_version_endpoint():
    handler = MagicMock()
    handle_get(handler, "/version")
    
    handler.send_json_response.assert_called_once_with(200, {"version": zai_coder.__version__})

def test_server_health_endpoint():
    handler = MagicMock()
    handle_get(handler, "/health")
    
    handler.send_json_response.assert_called_once_with(200, {"status": "ok"})

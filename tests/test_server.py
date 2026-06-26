import threading
import time
import requests
import pytest
from zai_coder.server.app import run_server

@pytest.fixture(scope="module")
def server():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    
    server_thread = threading.Thread(target=run_server, args=("127.0.0.1", port), daemon=True)
    server_thread.start()
    time.sleep(0.5) # give server time to start
    yield f"http://127.0.0.1:{port}"

def test_health(server):
    res = requests.get(f"{server}/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

def test_version(server):
    res = requests.get(f"{server}/version")
    assert res.status_code == 200
    assert "version" in res.json()

def test_agents(server):
    res = requests.get(f"{server}/agents")
    assert res.status_code == 200
    assert "agents" in res.json()
    assert isinstance(res.json()["agents"], list)

def test_skills(server):
    res = requests.get(f"{server}/skills")
    assert res.status_code == 200
    assert "skills" in res.json()

def test_self_features(server):
    res = requests.get(f"{server}/self/features")
    assert res.status_code == 200
    assert "features" in res.json()

def test_self_status(server):
    res = requests.get(f"{server}/self/status")
    assert res.status_code == 200
    assert "status" in res.json()

def test_payload_too_large(server):
    data = {"text": "A" * 1024 * 1025}
    res = requests.post(f"{server}/ask", json=data)
    assert res.status_code == 413

def test_run_command_blocked(server):
    res = requests.post(f"{server}/run", json={"command": "rm -rf /"})
    assert res.status_code == 200
    assert "blocked_reason" in res.json()

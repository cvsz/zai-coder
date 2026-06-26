import json
from zai_coder.core.metrics import MetricsFormatter

def test_metrics_formatter():
    metrics = {
        "python_version": "3.12",
        "disk_usage": {"used_gb": 10},
        "ollama_available": True
    }
    
    # JSON test
    json_str = MetricsFormatter.to_json(metrics)
    assert json.loads(json_str)["python_version"] == "3.12"
    
    # Markdown test
    md_str = MetricsFormatter.to_markdown(metrics)
    assert "| Python Version | 3.12 |" in md_str
    assert "| Disk Usage | used_gb: 10 |" in md_str

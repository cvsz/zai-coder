import os
from pathlib import Path
from zai_coder.core.indexer import ProjectIndexer
from zai_coder.core.rag import LocalRAG

def test_project_indexer(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    
    # Write some safe file
    (repo / "safe.py").write_text("class SafetyPolicy:\n    def check(self):\n        pass\n", encoding="utf-8")
    
    # Write some excluded file
    (repo / ".env").write_text("SECRET=ENVONLY999\n", encoding="utf-8")
    
    # Write some file with secrets
    secret = "s" + "k-12345678901234567890123456"
    (repo / "api_keys.py").write_text(f"API_KEY = '{secret}'\n", encoding="utf-8")
    
    # DB path
    db_path = tmp_path / "index.db"
    
    # Build index
    indexer = ProjectIndexer(workspace=repo, db_path=db_path)
    indexer.build()
    
    stats = indexer.get_stats()
    assert stats["files"] >= 1
    assert stats["chunks"] >= 1
    assert stats["symbols"] >= 1
    
    # Test index search
    results, metrics = indexer.search("SafetyPolicy")
    assert len(results) > 0
    assert "safe.py" in results[0]["path"]
    assert any(r["type"] == "symbol" for r in results)
    
    # Check that .env is not indexed
    env_results, _ = indexer.search("envonly999")
    assert len(env_results) == 0
    
    # Check that secret is redacted
    secret_results, _ = indexer.search("sk-")
    assert len(secret_results) == 0
    
    redacted_results, _ = indexer.search("REDACTED")
    assert len(redacted_results) > 0

    # Test clear
    indexer.clear()
    stats = indexer.get_stats()
    assert stats["files"] == 0
    assert stats["chunks"] == 0
    assert stats["symbols"] == 0

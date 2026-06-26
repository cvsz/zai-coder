import os
from pathlib import Path
from zai_coder.core.indexer import ProjectIndexer
from zai_coder.core.rag import LocalRAG

def test_indexing_and_rag(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    
    # Write some safe file
    (repo / "safe.py").write_text("def command_safety():\n    return 'Command safety is enforced here.'\n", encoding="utf-8")
    
    # Write some excluded file
    (repo / ".env").write_text("SECRET=ENVONLY999\n", encoding="utf-8")
    
    # Write some file with secrets
    secret = "s" + "k-12345678901234567890123456"
    (repo / "secret_file.py").write_text(f"API_KEY = '{secret}'\n", encoding="utf-8")
    
    # DB path
    db_path = tmp_path / "index.db"
    
    # Build index
    indexer = ProjectIndexer(db_path)
    indexer.build(repo)
    
    # Test index search
    results, metrics = indexer.search("safety")
    assert len(results) > 0
    assert "safe.py" in results[0]["path"]
    assert "time_ms" in metrics
    
    # Check that .env is not indexed
    env_results, _ = indexer.search("envonly999")
    assert len(env_results) == 0
    
    # Check that secret is redacted
    secret_results, _ = indexer.search("sk-")
    assert len(secret_results) == 0
    
    redacted_results, _ = indexer.search("REDACTED")
    assert len(redacted_results) > 0
    
    # Test RAG
    rag = LocalRAG(tmp_path)
    # patch rag.db_path for test
    rag.db_path = db_path
    rag.indexer = indexer
    
    res = rag.query("command safety")
    assert "Command safety is enforced here" in res

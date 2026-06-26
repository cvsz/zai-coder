import pytest
from zai_coder.core.rag import LocalRAG

def test_rag(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "safety.py").write_text("class Safety:\n    def command_safety(self):\n        pass", encoding="utf-8")
    
    rag = LocalRAG(repo)
    rag.db_path = tmp_path / "index.db"
    rag.indexer.db_path = rag.db_path
    
    rag.build()
    
    res = rag.query("command_safety")
    assert "safety.py" in res
    assert "Metrics:" in res

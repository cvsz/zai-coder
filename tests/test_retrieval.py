import pytest
from zai_coder.core.indexer import ProjectIndexer
from zai_coder.core.retrieval import RetrievalAugmentedGenerator

def test_retrieval(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "test.py").write_text("class Hello:\n    def world(self):\n        return 'hello'", encoding="utf-8")
    
    db_path = tmp_path / "index.db"
    indexer = ProjectIndexer(workspace=repo, db_path=db_path)
    indexer.build()
    
    retrieval = RetrievalAugmentedGenerator(indexer)
    context = retrieval.get_context("Hello")
    assert "File: test.py (line 1)" in context
    assert "Symbol: class Hello" in context
    
    context2 = retrieval.get_context("world")
    assert "world" in context2

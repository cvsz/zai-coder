from pathlib import Path
from zai_coder.core.indexer import ProjectIndexer
from zai_coder.core.retrieval import RetrievalAugmentedGenerator

class LocalRAG:
    def __init__(self, workspace: str | Path):
        self.workspace = Path(workspace).resolve()
        self.db_path = self.workspace / ".zai-coder" / "index" / "project-index.db"
        self.indexer = ProjectIndexer(workspace=self.workspace, db_path=self.db_path)
        self.retrieval = RetrievalAugmentedGenerator(self.indexer)

    def build(self):
        self.indexer.build()

    def query(self, query: str, limit: int = 5) -> str:
        # Build if index doesn't exist
        if not self.db_path.exists():
            self.build()
        
        results, metrics = self.indexer.search(query, limit)
        if not results:
            return "No relevant context found.\nMetrics: " + str(metrics)
        
        context = []
        for r in results:
            if r.get("type") == "symbol":
                context.append(f"File: {r['path']} (line {r['line']})\nSymbol: {r['symbol_type']} {r['name']}")
            else:
                context.append(f"File: {r['path']} (lines {r['start_line']}-{r['end_line']})\n```\n{r['text']}\n```")
        
        context.append(f"\n--- Retrieval Metrics ---\nTime: {metrics['time_ms']}ms\nChunks Scanned: {metrics['chunks_scanned']}\nChunks Matched: {metrics['chunks_matched']}\nTop Score: {metrics['top_score']}")
        return "\n".join(context)

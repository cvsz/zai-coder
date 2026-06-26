from pathlib import Path
from zai_coder.core.indexer import ProjectIndexer

class LocalRAG:
    def __init__(self, workspace: str | Path):
        self.workspace = Path(workspace).resolve()
        self.db_path = self.workspace / "data" / "index.db"
        self.indexer = ProjectIndexer(self.db_path)

    def build(self):
        self.indexer.build(self.workspace)

    def query(self, query: str, limit: int = 5) -> str:
        results, metrics = self.indexer.search(query, limit)
        if not results:
            return "No relevant context found.\nMetrics: " + str(metrics)
        
        context = []
        for r in results:
            context.append(f"File: {r['path']} (lines {r['start_line']}-{r['end_line']})\n```\n{r['text']}\n```\n")
        
        context.append(f"\n--- Retrieval Metrics ---\nTime: {metrics['time_ms']}ms\nChunks Scanned: {metrics['chunks_scanned']}\nChunks Matched: {metrics['chunks_matched']}\nTop Score: {metrics['top_score']}")
        return "\n".join(context)

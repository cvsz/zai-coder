from typing import Any
from pathlib import Path

class RetrievalAugmentedGenerator:
    def __init__(self, indexer):
        self.indexer = indexer
        
    def get_context(self, query: str, limit: int = 5) -> str:
        results, metrics = self.indexer.search(query, limit)
        if not results:
            return "No relevant context found."
            
        context = []
        for r in results:
            if r.get("type") == "symbol":
                context.append(f"File: {r['path']} (line {r['line']})\nSymbol: {r['symbol_type']} {r['name']}\n")
            else:
                context.append(f"File: {r['path']} (lines {r['start_line']}-{r['end_line']})\n```\n{r['text']}\n```\n")
                
        return "\n".join(context)

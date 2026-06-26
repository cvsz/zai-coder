import sqlite3
import hashlib
import time
from pathlib import Path
from zai_coder.core.redaction import redact_text

EXCLUDES = {
    ".git", ".venv", "node_modules", "dist", "out", "reports", "__pycache__", ".pytest_cache"
}
EXCLUDE_EXTS = {
    ".pyc", ".pyo", ".tgz", ".zip", ".tar", ".gz", ".sqlite3", ".db", ".png", ".jpg", ".svg", ".wav", ".jsonl"
}
EXCLUDE_NAMES = {
    ".env", ".env.local"
}

def is_ignored(path: Path, root: Path) -> bool:
    try:
        rel = path.relative_to(root)
    except ValueError:
        return True
    
    if any(part in EXCLUDES for part in rel.parts):
        return True
    if path.name in EXCLUDE_NAMES or path.name.startswith(".env"):
        return True
    if path.suffix in EXCLUDE_EXTS:
        return True
    return False

def hash_file(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

class ProjectIndexer:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self._init_db()

    def _init_db(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS file_index (
                    file_path TEXT PRIMARY KEY,
                    file_hash TEXT,
                    ext TEXT,
                    last_indexed REAL
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS chunk_index (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT,
                    chunk_text TEXT,
                    start_line INTEGER,
                    end_line INTEGER,
                    FOREIGN KEY(file_path) REFERENCES file_index(file_path)
                )
            """)

    def build(self, root: str | Path):
        root = Path(root).resolve()
        now = time.time()
        for p in root.rglob("*"):
            if not p.is_file():
                continue
            if is_ignored(p, root):
                continue
            
            try:
                text = p.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            
            rel_path = str(p.relative_to(root))
            fhash = hash_file(text)
            
            # Check if updated
            cur = self.conn.execute("SELECT file_hash FROM file_index WHERE file_path = ?", (rel_path,))
            row = cur.fetchone()
            if row and row[0] == fhash:
                continue
            
            text = redact_text(text)
            
            with self.conn:
                self.conn.execute("DELETE FROM chunk_index WHERE file_path = ?", (rel_path,))
                self.conn.execute("INSERT OR REPLACE INTO file_index (file_path, file_hash, ext, last_indexed) VALUES (?, ?, ?, ?)",
                                  (rel_path, fhash, p.suffix, now))
                
                # Naive chunking by lines (e.g. 50 lines)
                lines = text.splitlines()
                chunk_size = 50
                for i in range(0, len(lines), chunk_size):
                    chunk = "\n".join(lines[i:i+chunk_size])
                    self.conn.execute(
                        "INSERT INTO chunk_index (file_path, chunk_text, start_line, end_line) VALUES (?, ?, ?, ?)",
                        (rel_path, chunk, i+1, i+len(lines[i:i+chunk_size]))
                    )

    def search(self, query: str, limit: int = 10) -> tuple[list[dict], dict]:
        t0 = time.time()
        query = query.lower()
        terms = query.split()
        if not terms:
            return [], {"time_ms": 0, "chunks_scanned": 0, "chunks_matched": 0, "top_score": 0}
            
        cur = self.conn.cursor()
        cur.execute("SELECT file_path, chunk_text, start_line, end_line FROM chunk_index")
        
        results = []
        chunks_scanned = 0
        
        for row in cur.fetchall():
            chunks_scanned += 1
            path, text, start, end = row
            text_lower = text.lower()
            path_lower = path.lower()
            
            score = 0
            for term in terms:
                if term in text_lower:
                    score += text_lower.count(term)
                if term in path_lower:
                    score += 5
            
            if score > 0:
                results.append({
                    "path": path,
                    "text": text,
                    "start_line": start,
                    "end_line": end,
                    "score": score
                })
        
        results.sort(key=lambda x: x["score"], reverse=True)
        results = results[:limit]
        
        t1 = time.time()
        metrics = {
            "time_ms": int((t1 - t0) * 1000),
            "chunks_scanned": chunks_scanned,
            "chunks_matched": len(results),
            "top_score": results[0]["score"] if results else 0
        }
        return results, metrics

import sqlite3
import os
import time
from pathlib import Path
from typing import Any

from .file_fingerprint import get_file_fingerprint, should_ignore_file
from .language_detect import detect_language, extract_symbols
from .redaction import redact_text

class ProjectIndexer:
    def __init__(self, workspace: str | Path = None, db_path: str | Path = None):
        if workspace:
            self.workspace = Path(workspace).resolve()
        else:
            self.workspace = Path.cwd()
            
        if db_path is None:
            self.db_path = self.workspace / ".zai-coder" / "index" / "project-index.db"
        else:
            self.db_path = Path(db_path)
            
        self.conn = None

    def connect(self):
        if self.conn:
            return
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT UNIQUE,
                    sha256 TEXT,
                    size_bytes INTEGER,
                    language TEXT,
                    indexed_at REAL
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS chunks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_id INTEGER,
                    path TEXT,
                    start_line INTEGER,
                    end_line INTEGER,
                    text TEXT,
                    text_hash TEXT,
                    FOREIGN KEY(file_id) REFERENCES files(id) ON DELETE CASCADE
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS symbols (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_id INTEGER,
                    path TEXT,
                    symbol_type TEXT,
                    name TEXT,
                    line INTEGER,
                    FOREIGN KEY(file_id) REFERENCES files(id) ON DELETE CASCADE
                )
            """)

    def clear(self):
        self.connect()
        with self.conn:
            self.conn.execute("DROP TABLE IF EXISTS chunks")
            self.conn.execute("DROP TABLE IF EXISTS symbols")
            self.conn.execute("DROP TABLE IF EXISTS files")
        self._init_db()

    def build(self, root: str | Path = None):
        if root:
            self.workspace = Path(root).resolve()
            
        self.connect()
        
        all_files = []
        for r, dirs, files in os.walk(str(self.workspace)):
            dirs[:] = [d for d in dirs if not should_ignore_file(Path(r) / d)]
            for file in files:
                p = Path(r) / file
                if not p.is_symlink() and not should_ignore_file(p):
                    all_files.append(p)
                    
        now = time.time()
        for p in all_files:
            try:
                rel_path = str(p.relative_to(self.workspace)).replace("\\", "/")
                
                cur = self.conn.execute("SELECT id, sha256 FROM files WHERE path = ?", (rel_path,))
                row = cur.fetchone()
                
                current_sha = get_file_fingerprint(p)
                if not current_sha:
                    continue
                    
                if row and row["sha256"] == current_sha:
                    continue
                    
                try:
                    text = p.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    continue
                    
                text = redact_text(text)
                size = p.stat().st_size
                lang = detect_language(p)
                
                with self.conn:
                    if row:
                        file_id = row["id"]
                        self.conn.execute("DELETE FROM chunks WHERE file_id = ?", (file_id,))
                        self.conn.execute("DELETE FROM symbols WHERE file_id = ?", (file_id,))
                        self.conn.execute("UPDATE files SET sha256 = ?, size_bytes = ?, language = ?, indexed_at = ? WHERE id = ?",
                                       (current_sha, size, lang, now, file_id))
                    else:
                        cur = self.conn.execute("INSERT INTO files (path, sha256, size_bytes, language, indexed_at) VALUES (?, ?, ?, ?, ?)",
                                       (rel_path, current_sha, size, lang, now))
                        file_id = cur.lastrowid
                        
                    lines = text.splitlines()
                    chunk_size = 50
                    for i in range(0, len(lines), chunk_size):
                        chunk_text = "\n".join(lines[i:i+chunk_size])
                        import hashlib
                        chunk_hash = hashlib.sha256(chunk_text.encode()).hexdigest()
                        self.conn.execute(
                            "INSERT INTO chunks (file_id, path, start_line, end_line, text, text_hash) VALUES (?, ?, ?, ?, ?, ?)",
                            (file_id, rel_path, i+1, i+len(lines[i:i+chunk_size]), chunk_text, chunk_hash)
                        )
                        
                    symbols = extract_symbols(text, lang)
                    for sym_type, name, line in symbols:
                        self.conn.execute("INSERT INTO symbols (file_id, path, symbol_type, name, line) VALUES (?, ?, ?, ?, ?)",
                                       (file_id, rel_path, sym_type, name, line))
            except Exception:
                pass

    def search(self, query: str, limit: int = 10) -> tuple[list[dict], dict]:
        t0 = time.time()
        self.connect()
        query = query.lower()
        terms = query.split()
        if not terms:
            return [], {"time_ms": 0, "chunks_scanned": 0, "chunks_matched": 0, "top_score": 0}
            
        cur = self.conn.cursor()
        
        results = []
        chunks_scanned = 0
        
        # Search chunks
        cur.execute("SELECT path, start_line, end_line, text FROM chunks")
        for row in cur.fetchall():
            chunks_scanned += 1
            path = row["path"]
            text = row["text"]
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
                    "type": "text",
                    "path": path,
                    "text": text,
                    "start_line": row["start_line"],
                    "end_line": row["end_line"],
                    "score": score
                })
                
        # Search symbols
        cur.execute("SELECT path, symbol_type, name, line FROM symbols")
        for row in cur.fetchall():
            path = row["path"]
            name = row["name"].lower()
            path_lower = path.lower()
            score = 0
            for term in terms:
                if term in name:
                    score += 10
                if term in path_lower:
                    score += 5
            if score > 0:
                results.append({
                    "type": "symbol",
                    "path": path,
                    "symbol_type": row["symbol_type"],
                    "name": row["name"],
                    "line": row["line"],
                    "start_line": row["line"],
                    "end_line": row["line"],
                    "score": score,
                    "text": f"[{row['symbol_type']}] {row['name']} at line {row['line']}"
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

    def get_stats(self) -> dict[str, int]:
        self.connect()
        stats = {}
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM files")
        stats["files"] = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM chunks")
        stats["chunks"] = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM symbols")
        stats["symbols"] = cur.fetchone()[0]
        return stats

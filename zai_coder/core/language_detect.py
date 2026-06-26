import re
from pathlib import Path

def detect_language(filepath: str | Path) -> str:
    name = Path(filepath).name.lower()
    if name.endswith(".py"):
        return "python"
    elif name.endswith(".js"):
        return "javascript"
    elif name.endswith(".ts"):
        return "typescript"
    elif name.endswith((".jsx", ".tsx")):
        return "react"
    elif name.endswith(".sh") or name == "makefile":
        return "shell"
    elif name.endswith((".json", ".yaml", ".yml", ".md", ".txt")):
        return "data"
    elif name.endswith((".c", ".h", ".cpp", ".hpp", ".go", ".rs", ".java")):
        return "compiled"
    return "unknown"
    
def extract_symbols(content: str, language: str) -> list[tuple[str, str, int]]:
    """Returns list of (symbol_type, name, line_number)"""
    symbols = []
    lines = content.split('\n')
    
    if language == "python":
        class_re = re.compile(r"^\s*class\s+([A-Za-z0-9_]+)")
        def_re = re.compile(r"^\s*def\s+([A-Za-z0-9_]+)")
        for i, line in enumerate(lines, 1):
            m = class_re.search(line)
            if m:
                symbols.append(("class", m.group(1), i))
            m = def_re.search(line)
            if m:
                symbols.append(("function", m.group(1), i))
                
    elif language in ("javascript", "typescript", "react"):
        func_re = re.compile(r"^\s*(?:export\s+)?(?:async\s+)?function\s+([A-Za-z0-9_]+)")
        class_re = re.compile(r"^\s*(?:export\s+)?class\s+([A-Za-z0-9_]+)")
        const_re = re.compile(r"^\s*(?:export\s+)?const\s+([A-Za-z0-9_]+)\s*=\s*(?:\([^)]*\)|[A-Za-z0-9_]+)\s*=>")
        for i, line in enumerate(lines, 1):
            m = func_re.search(line)
            if m:
                symbols.append(("function", m.group(1), i))
            m = class_re.search(line)
            if m:
                symbols.append(("class", m.group(1), i))
            m = const_re.search(line)
            if m:
                symbols.append(("function", m.group(1), i))
                
    return symbols

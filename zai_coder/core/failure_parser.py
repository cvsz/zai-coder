import re
from typing import Dict, Any, List

class FailureParser:
    def __init__(self):
        self.pytest_regex = re.compile(r"FAILED\s+(.*?)::(.*?)\s+-\s+(.*)")
        self.compileall_regex = re.compile(r"Compiling\s+'(.*?)'\.\.\.\s*\n\s*SyntaxError:\s*(.*)")
        self.tb_regex = re.compile(r"File \"(.*?)\", line (\d+), in (.*)")

    def parse(self, output: str) -> List[Dict[str, Any]]:
        failures = []
        
        # Parse pytest failures
        for match in self.pytest_regex.finditer(output):
            failures.append({
                "type": "pytest",
                "file": match.group(1),
                "test": match.group(2),
                "error": match.group(3).strip()
            })
            
        # Parse compileall syntax errors
        # This one is tricky because it spans lines. We will just look for SyntaxError.
        lines = output.splitlines()
        for i, line in enumerate(lines):
            if "SyntaxError:" in line:
                file_path = "unknown"
                # Look back a few lines for the file
                for j in range(i-1, max(-1, i-5), -1):
                    if "Compiling" in lines[j] or "File" in lines[j]:
                        file_path = lines[j].replace("Compiling", "").replace("'", "").replace("...", "").strip()
                        break
                failures.append({
                    "type": "compile",
                    "file": file_path,
                    "error": line.strip()
                })
                
        # Fallback parse tracebacks
        if not failures:
            for match in self.tb_regex.finditer(output):
                failures.append({
                    "type": "traceback",
                    "file": match.group(1),
                    "line": match.group(2),
                    "context": match.group(3).strip()
                })
                
        if not failures and ("Error" in output or "Exception" in output or "FAIL" in output):
            failures.append({
                "type": "generic",
                "error": "Generic failure detected, check logs."
            })
            
        return failures

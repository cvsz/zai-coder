from pathlib import Path
from zai_coder.core.safety import SafetyPolicy
from zai_coder.core.context_files import ContextFileDiscoverer

def test_context_file_discoverer(tmp_path):
    safety = SafetyPolicy()
    discoverer = ContextFileDiscoverer(tmp_path, safety)
    
    # Create mock context files
    zai_md = tmp_path / ".zai.md"
    zai_md.write_text("Hello .zai.md")
    
    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text("Hello AGENTS.md")
    
    random_md = tmp_path / "RANDOM.md"
    random_md.write_text("Hello RANDOM.md")
    
    found = discoverer.discover()
    assert len(found) == 2
    assert zai_md in found
    assert agents_md in found
    assert random_md not in found
    
    content = discoverer.load(zai_md)
    assert content == "Hello .zai.md"

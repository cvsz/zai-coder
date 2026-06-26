import pytest
from zai_coder.core.command_parser import CommandParser, CommandParseError

def test_command_parser_safe():
    parser = CommandParser(workspace="/tmp")
    ctx = parser.parse("ls -l /tmp")
    assert ctx["name"] == "ls"
    assert ctx["args"] == ["ls", "-l", "/tmp"]
    assert ctx["cwd"] == "/tmp"

def test_command_parser_bypass_blocked():
    parser = CommandParser(workspace="/tmp")
    
    with pytest.raises(CommandParseError, match="Shell bypass token blocked"):
        parser.parse("echo hello ; rm -rf /")

    with pytest.raises(CommandParseError, match="Shell bypass token blocked"):
        parser.parse("cat file | grep secret")
        
    with pytest.raises(CommandParseError, match="Shell bypass token blocked"):
        parser.parse("ls && rm -rf /")
        
    with pytest.raises(CommandParseError, match="Shell bypass token blocked"):
        parser.parse("echo hello > out.txt")

def test_command_parser_substitution_blocked():
    parser = CommandParser(workspace="/tmp")
    
    with pytest.raises(CommandParseError, match="Shell substitution blocked"):
        parser.parse("echo $(cat .env)")
        
    with pytest.raises(CommandParseError, match="Shell substitution blocked"):
        parser.parse("echo `cat .env`")

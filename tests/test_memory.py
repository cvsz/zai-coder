from zai_coder.core.memory import MemoryStore


def test_memory_set_get_list(tmp_path):
    mem = MemoryStore(tmp_path / "mem.sqlite3")
    mem.set("goal", "ship", "project")
    assert mem.get("goal", "project") == "ship"
    items = mem.list("project")
    assert items[0].key == "goal"
    assert mem.delete("goal", "project") is True

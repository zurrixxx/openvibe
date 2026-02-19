import tempfile
from pathlib import Path


def test_read_messaging_framework():
    from vibe_inc.tools.shared_memory import read_memory

    # Use actual shared_memory dir
    memory_dir = Path(__file__).parent.parent / "shared_memory"
    result = read_memory("messaging/bot-framework.yaml", memory_dir=memory_dir)
    assert result["product"] == "Vibe Bot"


def test_write_and_read_performance():
    from vibe_inc.tools.shared_memory import read_memory, write_memory

    with tempfile.TemporaryDirectory() as tmpdir:
        data = {"bot": {"net_new_cac": 380, "known_cac": 220, "date": "2026-02-19"}}
        write_memory("performance/cac-latest.yaml", data, memory_dir=Path(tmpdir))
        result = read_memory("performance/cac-latest.yaml", memory_dir=Path(tmpdir))
        assert result["bot"]["net_new_cac"] == 380


def test_read_memory_has_docstring():
    from vibe_inc.tools.shared_memory import read_memory
    assert read_memory.__doc__ is not None


def test_write_memory_has_docstring():
    from vibe_inc.tools.shared_memory import write_memory
    assert write_memory.__doc__ is not None

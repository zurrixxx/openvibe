import yaml
from pathlib import Path

MEMORY_DIR = Path(__file__).parent.parent / "shared_memory"


def test_bot_framework_loads():
    path = MEMORY_DIR / "messaging" / "bot-framework.yaml"
    assert path.exists(), f"Missing: {path}"
    data = yaml.safe_load(path.read_text())
    assert data["product"] == "Vibe Bot"
    assert "positioning" in data
    assert "primary" in data["positioning"]


def test_icp_definitions_loads():
    path = MEMORY_DIR / "audiences" / "icp-definitions.yaml"
    assert path.exists(), f"Missing: {path}"
    data = yaml.safe_load(path.read_text())
    assert "bot" in data
    assert "dot" in data


def test_cac_benchmarks_loads():
    path = MEMORY_DIR / "performance" / "cac-benchmarks.yaml"
    assert path.exists(), f"Missing: {path}"
    data = yaml.safe_load(path.read_text())
    assert "bot" in data
    assert "target_cac" in data["bot"]

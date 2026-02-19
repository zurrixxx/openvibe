"""Shared memory tools — YAML-based cross-role memory for Phase 1."""
from pathlib import Path
import yaml

_DEFAULT_MEMORY_DIR = Path(__file__).resolve().parents[3] / "shared_memory"


def read_memory(path: str, memory_dir: Path | None = None) -> dict:
    """Read a shared memory file (YAML).

    Args:
        path: Relative path within shared_memory/ (e.g. 'messaging/bot-framework.yaml').
        memory_dir: Override memory directory (for testing). Default: vibe-inc/shared_memory/.

    Returns:
        Parsed YAML content as dict.
    """
    base = memory_dir or _DEFAULT_MEMORY_DIR
    file_path = base / path
    if not file_path.exists():
        return {}
    return yaml.safe_load(file_path.read_text()) or {}


def write_memory(path: str, data: dict, memory_dir: Path | None = None) -> dict:
    """Write data to a shared memory file (YAML).

    Args:
        path: Relative path within shared_memory/ (e.g. 'performance/cac-latest.yaml').
        data: Dict to write as YAML.
        memory_dir: Override memory directory (for testing).

    Returns:
        Dict with written=True and the path.
    """
    base = memory_dir or _DEFAULT_MEMORY_DIR
    file_path = base / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(yaml.dump(data, default_flow_style=False, allow_unicode=True))
    return {"written": True, "path": str(path)}

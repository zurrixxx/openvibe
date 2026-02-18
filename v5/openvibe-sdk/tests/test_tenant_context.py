from pathlib import Path
from openvibe_sdk.models import TenantContext


def test_tenant_context_fields():
    t = TenantContext(id="vibe-inc", name="Vibe Inc", data_dir=Path("/tmp/vibe"))
    assert t.id == "vibe-inc"
    assert t.name == "Vibe Inc"
    assert t.data_dir == Path("/tmp/vibe")


def test_tenant_context_default_data_dir():
    t = TenantContext(id="astrocrest", name="Astrocrest")
    assert t.data_dir == Path.home() / ".openvibe" / "astrocrest"


def test_tenant_context_slug():
    t = TenantContext(id="vibe-inc", name="Vibe Inc")
    assert t.id == "vibe-inc"  # id is the slug

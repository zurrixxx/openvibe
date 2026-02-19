import yaml
from pathlib import Path

_MEMORY_DIR = Path(__file__).parent.parent / "shared_memory"


def test_catalog_yaml_exists():
    path = _MEMORY_DIR / "data" / "catalog.yaml"
    assert path.exists(), f"Missing: {path}"
    data = yaml.safe_load(path.read_text())
    assert "tables" in data


def test_catalog_has_ads_fact():
    path = _MEMORY_DIR / "data" / "catalog.yaml"
    data = yaml.safe_load(path.read_text())
    tables = {t["name"]: t for t in data["tables"]}
    assert "fct_ads_ad_metrics" in tables
    tbl = tables["fct_ads_ad_metrics"]
    assert tbl["schema"] == "common"
    cols = {c["name"] for c in tbl["columns"]}
    assert "spend_in_usd" in cols
    assert "impressions" in cols
    assert "platform" in cols
    assert "purchase_count" in cols


def test_catalog_has_order_fact():
    path = _MEMORY_DIR / "data" / "catalog.yaml"
    data = yaml.safe_load(path.read_text())
    tables = {t["name"]: t for t in data["tables"]}
    assert "fct_order" in tables
    cols = {c["name"] for c in tables["fct_order"]["columns"]}
    assert "net_sales" in cols
    assert "platform" in cols


def test_catalog_has_website_session():
    path = _MEMORY_DIR / "data" / "catalog.yaml"
    data = yaml.safe_load(path.read_text())
    tables = {t["name"]: t for t in data["tables"]}
    assert "fct_website_session" in tables
    cols = {c["name"] for c in tables["fct_website_session"]["columns"]}
    assert "session_traffic_channel" in cols
    assert "dim_ads_campaign_sk" in cols


def test_catalog_has_conversion_fact():
    path = _MEMORY_DIR / "data" / "catalog.yaml"
    data = yaml.safe_load(path.read_text())
    tables = {t["name"]: t for t in data["tables"]}
    assert "fct_website_visitor_conversion" in tables


def test_catalog_has_email_fact():
    path = _MEMORY_DIR / "data" / "catalog.yaml"
    data = yaml.safe_load(path.read_text())
    tables = {t["name"]: t for t in data["tables"]}
    assert "fct_email_event" in tables


def test_catalog_has_dimensions():
    path = _MEMORY_DIR / "data" / "catalog.yaml"
    data = yaml.safe_load(path.read_text())
    tables = {t["name"]: t for t in data["tables"]}
    assert "dim_ads_campaign" in tables
    assert "dim_ads_ad_group" in tables
    assert "dim_ads_ad" in tables


def test_catalog_has_field_mapping():
    path = _MEMORY_DIR / "data" / "field_mapping.yaml"
    assert path.exists(), f"Missing: {path}"
    data = yaml.safe_load(path.read_text())
    assert "conversion_names" in data
    assert "purchase" in data["conversion_names"]

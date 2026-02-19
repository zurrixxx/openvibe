# D2C Phase 1: D2C Growth — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build the D2C Growth role with AdOps and CROps operators, integrating Meta Ads API, GA4 Data API, and Shopify Admin API.

**Architecture:** Two operators (AdOps, CROps) under one Role (D2CGrowth), using @agent_node with real API tool functions. LangGraph workflows registered with RoleRuntime. Shared memory as YAML files on disk.

**Tech Stack:** Python 3.13, openvibe-sdk v1.0.0, anthropic, langgraph, facebook-business, google-ads, google-analytics-data, ShopifyAPI, pyyaml, python-dotenv

**Design Doc:** `v5/docs/plans/2026-02-19-d2c-marketing-adoption.md`

---

## Task Overview

| # | Task | Files | Tests |
|---|------|-------|-------|
| 1 | Project scaffold + dependencies | vibe-inc/pyproject.toml, package structure | — |
| 2 | Shared memory YAML bootstrap | vibe-inc/shared_memory/*.yaml | 3 tests |
| 3 | Meta Ads read tool | vibe-inc/tools/meta_ads.py | 4 tests |
| 4 | Meta Ads write tools | vibe-inc/tools/meta_ads.py | 4 tests |
| 5 | GA4 read tool | vibe-inc/tools/ga4.py | 3 tests |
| 6 | Shopify tools | vibe-inc/tools/shopify.py | 4 tests |
| 7 | AdOps operator — campaign_create | vibe-inc/roles/d2c_growth/ad_ops.py | 3 tests |
| 8 | AdOps operator — daily_optimize | vibe-inc/roles/d2c_growth/ad_ops.py | 3 tests |
| 9 | AdOps operator — weekly_report | vibe-inc/roles/d2c_growth/ad_ops.py | 2 tests |
| 10 | CROps operator — experiment_analyze | vibe-inc/roles/d2c_growth/cro_ops.py | 3 tests |
| 11 | CROps operator — funnel_diagnose | vibe-inc/roles/d2c_growth/cro_ops.py | 2 tests |
| 12 | CROps operator — page_optimize | vibe-inc/roles/d2c_growth/cro_ops.py | 3 tests |
| 13 | D2CGrowth role class | vibe-inc/roles/d2c_growth/__init__.py | 4 tests |
| 14 | LangGraph workflow factories | vibe-inc/roles/d2c_growth/workflows.py | 4 tests |
| 15 | RoleRuntime wiring + activation | vibe-inc/main.py | 3 tests |
| 16 | Shared memory read/write helpers | vibe-inc/tools/shared_memory.py | 4 tests |
| 17 | Integration test — full loop | vibe-inc/tests/test_integration.py | 2 tests |

**Total: ~51 tests across 17 tasks**

---

### Task 1: Project Scaffold + Dependencies

**Files:**
- Create: `v5/vibe-inc/pyproject.toml`
- Create: `v5/vibe-inc/roles/__init__.py`
- Create: `v5/vibe-inc/roles/d2c_growth/__init__.py` (empty placeholder)
- Create: `v5/vibe-inc/tools/__init__.py`
- Create: `v5/vibe-inc/tests/__init__.py`
- Create: `v5/vibe-inc/.env.example`
- Create: `v5/vibe-inc/.gitignore`

**Step 1: Create pyproject.toml**

```toml
[project]
name = "vibe-inc"
version = "0.1.0"
description = "Vibe Inc D2C marketing roles on OpenVibe V5"
requires-python = ">=3.13"
dependencies = [
    "openvibe-sdk>=1.0.0",
    "openvibe-runtime>=1.0.0",
    "facebook-business>=20.0.0",
    "google-ads>=25.0.0",
    "google-analytics-data>=0.18.0",
    "ShopifyAPI>=12.0.0",
    "python-dotenv>=1.0.0",
    "pyyaml>=6.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-mock>=3.12",
]

[build-system]
requires = ["setuptools>=75.0"]
build-backend = "setuptools.backends._legacy:_Backend"
```

**Step 2: Create package structure**

```bash
mkdir -p v5/vibe-inc/{roles/d2c_growth,tools,tests,shared_memory/{messaging,audiences,competitive/battlecards,performance,content}}
touch v5/vibe-inc/{roles,roles/d2c_growth,tools,tests}/__init__.py
```

**Step 3: Create .env.example**

```bash
# Meta Ads API
META_APP_ID=
META_APP_SECRET=
META_ACCESS_TOKEN=
META_AD_ACCOUNT_ID=

# GA4 Data API
GA4_PROPERTY_ID=
GA4_SERVICE_ACCOUNT_JSON=

# Shopify Admin API
SHOPIFY_STORE=
SHOPIFY_ACCESS_TOKEN=
```

**Step 4: Create .gitignore**

```
.env
secrets.env
__pycache__/
*.pyc
```

**Step 5: Install in dev mode**

Run: `cd v5 && pip install -e "vibe-inc[dev]"`
Expected: Successful install with all dependencies

**Step 6: Commit**

```bash
git add v5/vibe-inc/
git commit -m "feat(vibe-inc): scaffold D2C Phase 1 project structure"
```

---

### Task 2: Shared Memory YAML Bootstrap

**Files:**
- Create: `v5/vibe-inc/shared_memory/messaging/bot-framework.yaml`
- Create: `v5/vibe-inc/shared_memory/messaging/dot-framework.yaml`
- Create: `v5/vibe-inc/shared_memory/messaging/board-framework.yaml`
- Create: `v5/vibe-inc/shared_memory/performance/cac-benchmarks.yaml`
- Create: `v5/vibe-inc/shared_memory/audiences/icp-definitions.yaml`
- Test: `v5/vibe-inc/tests/test_shared_memory_bootstrap.py`

**Step 1: Write test for YAML loading**

```python
# v5/vibe-inc/tests/test_shared_memory_bootstrap.py
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
```

**Step 2: Run test to verify it fails**

Run: `pytest v5/vibe-inc/tests/test_shared_memory_bootstrap.py -v`
Expected: FAIL — files don't exist yet

**Step 3: Create bot-framework.yaml**

```yaml
# v5/vibe-inc/shared_memory/messaging/bot-framework.yaml
product: Vibe Bot
status: validating  # validating | locked | revising
positioning:
  primary: "The room that remembers for you"
  supporting:
    - "Every meeting outcome captured, every action tracked"
    - "Cross-platform: works with Zoom, Teams, Meet, in-person"
  proof_points:
    - "360° audio capture"
    - "AI action extraction, not just transcription"
    - "Integrates with Vibe Workspace for team memory"
narrative_test:
  status: in_progress
  variants:
    - id: control
      message: "Vibebot: AI Meeting Room Device"
    - id: pain
      message: "Why do we have the same meeting every week?"
    - id: foundation
      message: "The room that remembers for you"
    - id: future
      message: "Meetings that actually move forward"
  current_leader: foundation
  confidence: 0.72
  decision_date: "2026-03-07"
```

**Step 4: Create dot-framework.yaml**

```yaml
product: Vibe Dot
status: validating
positioning:
  primary: "Your brain is for thinking, not remembering"
  supporting:
    - "Always-on AI that captures conversations, thoughts, meetings"
    - "AI-powered retrieval — ask questions, get answers"
  proof_points:
    - "Portable, always-on"
    - "AI retrieval, not just playback"
    - "Integrates with Vibe Workspace"
narrative_test:
  status: in_progress
  variants:
    - id: line_a
      message: "Mental Bandwidth — You're taking notes OR listening. Pick one."
    - id: line_b
      message: "AI Helper — AI doesn't just record, it helps you remember"
  current_leader: line_a
  decision_date: "2026-03-14"
```

**Step 5: Create board-framework.yaml**

```yaml
product: Vibe Board
status: locked
positioning:
  primary: "Thoughts deserve to be seen"
  supporting:
    - "Google-first for K-12"
    - "Open ecosystem, not locked to Microsoft"
    - "AI-native with workspace integration"
  proof_points:
    - "40,000+ companies"
    - "Affordable alternative to Surface Hub"
    - "Dual-line positioning validated"
```

**Step 6: Create icp-definitions.yaml**

```yaml
bot:
  primary:
    title: "SMB Meeting-Heavy Manager"
    company_size: "50-200 employees"
    behavior: "10+ meetings per week"
    pain: "Action items lost, meetings repeated"
  secondary:
    title: "Sales Team Lead"
    behavior: "Client-facing meetings daily"
    pain: "No memory of what was promised"
dot:
  primary:
    title: "Knowledge Worker"
    behavior: "Constant context switching, ideas during commute/walk"
    pain: "Best ideas arrive when not ready to capture"
  secondary:
    title: "Sales Rep"
    behavior: "Client calls throughout day"
    pain: "Manual note-taking during conversations"
board:
  primary:
    title: "K-12 Administrator"
    behavior: "Classroom tech procurement"
    pain: "Legacy whiteboards, need Google integration"
```

**Step 7: Create cac-benchmarks.yaml**

```yaml
bot:
  target_cac: 400
  current_cac: null  # Not yet measured (Net New)
  blended_cac: null  # Current reported, unreliable
  target_cvr: 0.02
  target_revenue_per_visitor: 15
dot:
  target_cac: 300
  current_cac: null
  target_cvr: 0.01
  target_revenue_per_visitor: 3
board:
  target_cac: null  # D2C Board not primary focus
  current_cvr: 0.015
  target_cvr: 0.025
```

**Step 8: Run tests to verify they pass**

Run: `pytest v5/vibe-inc/tests/test_shared_memory_bootstrap.py -v`
Expected: 3 passed

**Step 9: Commit**

```bash
git add v5/vibe-inc/shared_memory/ v5/vibe-inc/tests/test_shared_memory_bootstrap.py
git commit -m "feat(vibe-inc): bootstrap shared memory YAML — messaging, ICP, CAC benchmarks"
```

---

### Task 3: Meta Ads Read Tool

**Files:**
- Create: `v5/vibe-inc/tools/meta_ads.py`
- Test: `v5/vibe-inc/tests/test_meta_ads.py`

**Step 1: Write failing tests**

```python
# v5/vibe-inc/tests/test_meta_ads.py
from unittest.mock import patch, MagicMock


def test_meta_ads_read_returns_campaign_data():
    """meta_ads_read returns structured performance data."""
    from vibe_inc.tools.meta_ads import meta_ads_read

    mock_campaign = MagicMock()
    mock_campaign.get_insights.return_value = [
        {"campaign_name": "Bot - Foundation", "spend": "150.00",
         "impressions": "10000", "clicks": "200", "actions": [{"action_type": "purchase", "value": "5"}]}
    ]
    mock_account = MagicMock()
    mock_account.get_campaigns.return_value = [mock_campaign]

    with patch("vibe_inc.tools.meta_ads._get_account", return_value=mock_account):
        result = meta_ads_read(level="campaign", date_range="last_7d")

    assert "rows" in result
    assert result["level"] == "campaign"


def test_meta_ads_read_has_docstring():
    """Tool function must have a docstring for Anthropic schema generation."""
    from vibe_inc.tools.meta_ads import meta_ads_read
    assert meta_ads_read.__doc__ is not None
    assert "Read" in meta_ads_read.__doc__


def test_meta_ads_read_accepts_date_range():
    """meta_ads_read accepts custom date ranges."""
    from vibe_inc.tools.meta_ads import meta_ads_read

    mock_account = MagicMock()
    mock_account.get_campaigns.return_value = []

    with patch("vibe_inc.tools.meta_ads._get_account", return_value=mock_account):
        result = meta_ads_read(level="campaign", date_range="2026-02-01,2026-02-15")

    assert result["date_range"] == "2026-02-01,2026-02-15"


def test_meta_ads_read_supports_adset_level():
    """meta_ads_read can report at adset level."""
    from vibe_inc.tools.meta_ads import meta_ads_read

    mock_account = MagicMock()
    mock_account.get_ad_sets.return_value = []

    with patch("vibe_inc.tools.meta_ads._get_account", return_value=mock_account):
        result = meta_ads_read(level="adset", date_range="last_7d")

    assert result["level"] == "adset"
```

**Step 2: Run test to verify it fails**

Run: `pytest v5/vibe-inc/tests/test_meta_ads.py -v`
Expected: FAIL — module not found

**Step 3: Implement meta_ads.py (read portion)**

```python
# v5/vibe-inc/tools/meta_ads.py
"""Meta Ads API tools for D2C Growth role."""
import os


def _get_account():
    """Initialize Meta Ads API client from environment.

    Requires: META_APP_ID, META_APP_SECRET, META_ACCESS_TOKEN, META_AD_ACCOUNT_ID
    """
    from facebook_business.api import FacebookAdsApi
    from facebook_business.adobjects.adaccount import AdAccount

    FacebookAdsApi.init(
        app_id=os.environ["META_APP_ID"],
        app_secret=os.environ["META_APP_SECRET"],
        access_token=os.environ["META_ACCESS_TOKEN"],
    )
    return AdAccount(f'act_{os.environ["META_AD_ACCOUNT_ID"]}')


_DEFAULT_FIELDS = [
    "campaign_name", "spend", "impressions", "clicks",
    "cpc", "cpm", "ctr", "actions", "cost_per_action_type",
]


def meta_ads_read(
    level: str = "campaign",
    date_range: str = "last_7d",
    fields: list[str] | None = None,
) -> dict:
    """Read Meta Ads performance data.

    Args:
        level: Reporting level — campaign, adset, or ad.
        date_range: Date range — last_24h, last_7d, last_30d, or YYYY-MM-DD,YYYY-MM-DD.
        fields: Metrics to retrieve (default: spend, impressions, clicks, cpc, cpm, ctr, actions).

    Returns:
        Dict with 'level', 'date_range', and 'rows' (list of performance records).
    """
    account = _get_account()
    report_fields = fields or _DEFAULT_FIELDS

    # Build date preset or time range
    params = {}
    if "," in date_range:
        start, end = date_range.split(",", 1)
        params["time_range"] = {"since": start.strip(), "until": end.strip()}
    else:
        params["date_preset"] = date_range

    rows = []
    if level == "campaign":
        for campaign in account.get_campaigns(fields=["name", "status"]):
            insights = campaign.get_insights(fields=report_fields, params=params)
            for row in insights:
                rows.append(dict(row))
    elif level == "adset":
        for adset in account.get_ad_sets(fields=["name", "status"]):
            insights = adset.get_insights(fields=report_fields, params=params)
            for row in insights:
                rows.append(dict(row))
    elif level == "ad":
        for ad in account.get_ads(fields=["name", "status"]):
            insights = ad.get_insights(fields=report_fields, params=params)
            for row in insights:
                rows.append(dict(row))

    return {"level": level, "date_range": date_range, "rows": rows}
```

**Step 4: Run tests to verify they pass**

Run: `pytest v5/vibe-inc/tests/test_meta_ads.py -v`
Expected: 4 passed

**Step 5: Commit**

```bash
git add v5/vibe-inc/tools/meta_ads.py v5/vibe-inc/tests/test_meta_ads.py
git commit -m "feat(vibe-inc): Meta Ads read tool with campaign/adset/ad levels"
```

---

### Task 4: Meta Ads Write Tools

**Files:**
- Modify: `v5/vibe-inc/tools/meta_ads.py`
- Test: `v5/vibe-inc/tests/test_meta_ads.py` (append)

**Step 1: Write failing tests**

```python
# Append to v5/vibe-inc/tests/test_meta_ads.py

def test_meta_ads_create_returns_ids():
    """meta_ads_create returns campaign, adset, and ad IDs."""
    from vibe_inc.tools.meta_ads import meta_ads_create

    mock_account = MagicMock()
    mock_campaign = MagicMock()
    mock_campaign.__getitem__ = MagicMock(return_value="camp_123")
    mock_account.create_campaign.return_value = mock_campaign

    mock_adset = MagicMock()
    mock_adset.__getitem__ = MagicMock(return_value="adset_456")

    mock_ad = MagicMock()
    mock_ad.__getitem__ = MagicMock(return_value="ad_789")

    with patch("vibe_inc.tools.meta_ads._get_account", return_value=mock_account), \
         patch("vibe_inc.tools.meta_ads._create_adset", return_value=mock_adset), \
         patch("vibe_inc.tools.meta_ads._create_ad", return_value=mock_ad):
        result = meta_ads_create(
            campaign_name="Bot - Foundation Test",
            objective="OUTCOME_SALES",
            budget_daily=50.0,
            targeting={"age_min": 25, "age_max": 55, "interests": ["technology"]},
            creative={"headline": "The room that remembers", "body": "Test body", "link": "https://vibe.us/bot"},
        )

    assert "campaign_id" in result
    assert "adset_id" in result
    assert "ad_id" in result


def test_meta_ads_create_has_docstring():
    from vibe_inc.tools.meta_ads import meta_ads_create
    assert meta_ads_create.__doc__ is not None


def test_meta_ads_update_changes_status():
    """meta_ads_update can pause a campaign."""
    from vibe_inc.tools.meta_ads import meta_ads_update

    mock_obj = MagicMock()
    mock_obj.api_update.return_value = True

    with patch("vibe_inc.tools.meta_ads._get_object", return_value=mock_obj):
        result = meta_ads_update(
            object_type="campaign",
            object_id="camp_123",
            updates={"status": "PAUSED"},
        )

    assert result["updated"] is True
    assert result["object_id"] == "camp_123"


def test_meta_ads_update_has_docstring():
    from vibe_inc.tools.meta_ads import meta_ads_update
    assert meta_ads_update.__doc__ is not None
```

**Step 2: Run test to verify it fails**

Run: `pytest v5/vibe-inc/tests/test_meta_ads.py::test_meta_ads_create_returns_ids -v`
Expected: FAIL — function not defined

**Step 3: Implement write functions**

Add to `v5/vibe-inc/tools/meta_ads.py`:

```python
def _create_adset(account, campaign_id: str, budget_daily: float, targeting: dict) -> dict:
    """Create an adset under a campaign."""
    from facebook_business.adobjects.adset import AdSet
    params = {
        "name": f"Adset - {campaign_id}",
        "campaign_id": campaign_id,
        "daily_budget": int(budget_daily * 100),  # cents
        "billing_event": "IMPRESSIONS",
        "optimization_goal": "OFFSITE_CONVERSIONS",
        "targeting": targeting,
        "status": "PAUSED",  # Start paused for review
    }
    return account.create_ad_set(fields=[], params=params)


def _create_ad(account, adset_id: str, creative: dict) -> dict:
    """Create an ad under an adset."""
    params = {
        "name": f"Ad - {adset_id}",
        "adset_id": adset_id,
        "creative": creative,
        "status": "PAUSED",
    }
    return account.create_ad(fields=[], params=params)


def _get_object(object_type: str, object_id: str):
    """Get a Meta Ads object by type and ID."""
    from facebook_business.adobjects.campaign import Campaign
    from facebook_business.adobjects.adset import AdSet
    from facebook_business.adobjects.ad import Ad

    classes = {"campaign": Campaign, "adset": AdSet, "ad": Ad}
    cls = classes.get(object_type)
    if not cls:
        raise ValueError(f"Unknown object_type: {object_type}")
    return cls(object_id)


def meta_ads_create(
    campaign_name: str,
    objective: str,
    budget_daily: float,
    targeting: dict,
    creative: dict,
) -> dict:
    """Create a new Meta Ads campaign with adset and ad.

    Args:
        campaign_name: Name for the campaign (e.g. 'Bot - Foundation Test').
        objective: Campaign objective (OUTCOME_SALES, OUTCOME_TRAFFIC, etc.).
        budget_daily: Daily budget in USD.
        targeting: Audience targeting spec (age_min, age_max, interests, etc.).
        creative: Ad creative dict (headline, body, image_url, link).

    Returns:
        Dict with campaign_id, adset_id, and ad_id. All created in PAUSED status.
    """
    account = _get_account()

    campaign = account.create_campaign(fields=[], params={
        "name": campaign_name,
        "objective": objective,
        "status": "PAUSED",
        "special_ad_categories": [],
    })
    campaign_id = campaign["id"]

    adset = _create_adset(account, campaign_id, budget_daily, targeting)
    adset_id = adset["id"]

    ad = _create_ad(account, adset_id, creative)
    ad_id = ad["id"]

    return {"campaign_id": campaign_id, "adset_id": adset_id, "ad_id": ad_id}


def meta_ads_update(
    object_type: str,
    object_id: str,
    updates: dict,
) -> dict:
    """Update a Meta Ads object (campaign, adset, or ad).

    Args:
        object_type: Type — campaign, adset, or ad.
        object_id: ID of the object to update.
        updates: Fields to update (status, daily_budget, bid_amount, name, etc.).

    Returns:
        Dict with updated=True and the object_id.
    """
    obj = _get_object(object_type, object_id)
    obj.api_update(fields=[], params=updates)
    return {"updated": True, "object_id": object_id, "updates": updates}
```

**Step 4: Run tests to verify they pass**

Run: `pytest v5/vibe-inc/tests/test_meta_ads.py -v`
Expected: 8 passed

**Step 5: Commit**

```bash
git add v5/vibe-inc/tools/meta_ads.py v5/vibe-inc/tests/test_meta_ads.py
git commit -m "feat(vibe-inc): Meta Ads create + update tools"
```

---

### Task 5: GA4 Read Tool

**Files:**
- Create: `v5/vibe-inc/tools/ga4.py`
- Test: `v5/vibe-inc/tests/test_ga4.py`

**Step 1: Write failing tests**

```python
# v5/vibe-inc/tests/test_ga4.py
from unittest.mock import patch, MagicMock


def test_ga4_read_returns_rows():
    """ga4_read returns metric rows."""
    from vibe_inc.tools.ga4 import ga4_read

    mock_response = MagicMock()
    mock_row = MagicMock()
    mock_row.dimension_values = [MagicMock(value="organic")]
    mock_row.metric_values = [MagicMock(value="1000"), MagicMock(value="50")]
    mock_response.rows = [mock_row]

    mock_client = MagicMock()
    mock_client.run_report.return_value = mock_response

    with patch("vibe_inc.tools.ga4._get_client", return_value=mock_client):
        result = ga4_read(
            metrics=["sessions", "conversions"],
            dimensions=["sessionDefaultChannelGroup"],
            date_range="last_7d",
        )

    assert "rows" in result
    assert len(result["rows"]) == 1


def test_ga4_read_has_docstring():
    from vibe_inc.tools.ga4 import ga4_read
    assert ga4_read.__doc__ is not None
    assert "GA4" in ga4_read.__doc__


def test_ga4_read_funnel_events():
    """ga4_read can query specific events for funnel analysis."""
    from vibe_inc.tools.ga4 import ga4_read

    mock_response = MagicMock()
    mock_response.rows = []
    mock_client = MagicMock()
    mock_client.run_report.return_value = mock_response

    with patch("vibe_inc.tools.ga4._get_client", return_value=mock_client):
        result = ga4_read(
            metrics=["eventCount"],
            dimensions=["eventName", "pagePath"],
            date_range="last_7d",
            dimension_filter={"eventName": ["pdp_view", "cta_click", "begin_checkout", "purchase"]},
        )

    assert result["rows"] == []
    # Verify the client was called with filter
    mock_client.run_report.assert_called_once()
```

**Step 2: Run test to verify it fails**

Run: `pytest v5/vibe-inc/tests/test_ga4.py -v`
Expected: FAIL — module not found

**Step 3: Implement ga4.py**

```python
# v5/vibe-inc/tools/ga4.py
"""GA4 Data API tools for D2C Growth role."""
import os


def _get_client():
    """Initialize GA4 Data API client.

    Requires: GA4_PROPERTY_ID and either GA4_SERVICE_ACCOUNT_JSON (file path)
    or default application credentials.
    """
    from google.analytics.data_v1beta import BetaAnalyticsDataClient

    sa_path = os.environ.get("GA4_SERVICE_ACCOUNT_JSON")
    if sa_path:
        return BetaAnalyticsDataClient.from_service_account_json(sa_path)
    return BetaAnalyticsDataClient()


def ga4_read(
    metrics: list[str],
    dimensions: list[str] | None = None,
    date_range: str = "last_7d",
    dimension_filter: dict[str, list[str]] | None = None,
) -> dict:
    """Read GA4 analytics data for Vibe's properties.

    Args:
        metrics: Metrics to query (e.g. sessions, conversions, eventCount).
        dimensions: Dimensions to group by (e.g. sessionDefaultChannelGroup, eventName, pagePath).
        date_range: Date range — last_7d, last_28d, last_90d, or YYYY-MM-DD,YYYY-MM-DD.
        dimension_filter: Optional filter dict mapping dimension name to allowed values.

    Returns:
        Dict with 'metrics', 'dimensions', 'date_range', and 'rows' (list of dicts).
    """
    from google.analytics.data_v1beta.types import (
        DateRange, Dimension, Filter, FilterExpression,
        FilterExpressionList, Metric, RunReportRequest,
    )

    client = _get_client()
    property_id = os.environ["GA4_PROPERTY_ID"]

    # Build date range
    if "," in date_range:
        start, end = date_range.split(",", 1)
        dr = DateRange(start_date=start.strip(), end_date=end.strip())
    else:
        days = {"last_7d": "7daysAgo", "last_28d": "28daysAgo", "last_90d": "90daysAgo"}
        dr = DateRange(start_date=days.get(date_range, "7daysAgo"), end_date="today")

    # Build request
    request = RunReportRequest(
        property=f"properties/{property_id}",
        metrics=[Metric(name=m) for m in metrics],
        dimensions=[Dimension(name=d) for d in (dimensions or [])],
        date_ranges=[dr],
    )

    # Add dimension filter if provided
    if dimension_filter:
        filters = []
        for dim_name, values in dimension_filter.items():
            filters.append(FilterExpression(
                filter=Filter(
                    field_name=dim_name,
                    in_list_filter=Filter.InListFilter(values=values),
                )
            ))
        if len(filters) == 1:
            request.dimension_filter = filters[0]
        else:
            request.dimension_filter = FilterExpression(
                and_group=FilterExpressionList(expressions=filters)
            )

    response = client.run_report(request)

    rows = []
    for row in response.rows:
        entry = {}
        for i, dim in enumerate(dimensions or []):
            entry[dim] = row.dimension_values[i].value
        for i, met in enumerate(metrics):
            entry[met] = row.metric_values[i].value
        rows.append(entry)

    return {
        "metrics": metrics,
        "dimensions": dimensions or [],
        "date_range": date_range,
        "rows": rows,
    }
```

**Step 4: Run tests to verify they pass**

Run: `pytest v5/vibe-inc/tests/test_ga4.py -v`
Expected: 3 passed

**Step 5: Commit**

```bash
git add v5/vibe-inc/tools/ga4.py v5/vibe-inc/tests/test_ga4.py
git commit -m "feat(vibe-inc): GA4 Data API read tool with funnel event filtering"
```

---

### Task 6: Shopify Tools

**Files:**
- Create: `v5/vibe-inc/tools/shopify.py`
- Test: `v5/vibe-inc/tests/test_shopify.py`

**Step 1: Write failing tests**

```python
# v5/vibe-inc/tests/test_shopify.py
from unittest.mock import patch, MagicMock


def test_shopify_page_read_returns_content():
    from vibe_inc.tools.shopify import shopify_page_read

    mock_page = {"id": 123, "title": "Vibebot", "body_html": "<h1>Bot</h1>"}
    with patch("vibe_inc.tools.shopify._get_page", return_value=mock_page):
        result = shopify_page_read(page_id="123")

    assert result["title"] == "Vibebot"
    assert "body_html" in result


def test_shopify_page_read_has_docstring():
    from vibe_inc.tools.shopify import shopify_page_read
    assert shopify_page_read.__doc__ is not None


def test_shopify_page_update_changes_content():
    from vibe_inc.tools.shopify import shopify_page_update

    mock_page = MagicMock()
    with patch("vibe_inc.tools.shopify._get_page_resource", return_value=mock_page):
        result = shopify_page_update(
            page_id="123",
            updates={"title": "New Title", "body_html": "<h1>Updated</h1>"},
        )

    assert result["updated"] is True
    assert result["page_id"] == "123"


def test_shopify_page_update_has_docstring():
    from vibe_inc.tools.shopify import shopify_page_update
    assert shopify_page_update.__doc__ is not None
```

**Step 2: Run test to verify it fails**

Run: `pytest v5/vibe-inc/tests/test_shopify.py -v`
Expected: FAIL

**Step 3: Implement shopify.py**

```python
# v5/vibe-inc/tools/shopify.py
"""Shopify Admin API tools for CROps operator."""
import os


def _get_session():
    """Create Shopify API session from environment.

    Requires: SHOPIFY_STORE, SHOPIFY_ACCESS_TOKEN
    """
    import shopify
    store = os.environ["SHOPIFY_STORE"]
    token = os.environ["SHOPIFY_ACCESS_TOKEN"]
    session = shopify.Session(f"{store}.myshopify.com", "2024-01", token)
    shopify.ShopifyResource.activate_session(session)
    return session


def _get_page(page_id: str) -> dict:
    """Fetch a page by ID."""
    import shopify
    _get_session()
    page = shopify.Page.find(page_id)
    return page.to_dict()


def _get_page_resource(page_id: str):
    """Fetch a page resource for updates."""
    import shopify
    _get_session()
    return shopify.Page.find(page_id)


def shopify_page_read(page_id: str) -> dict:
    """Read a Shopify page's content by ID.

    Args:
        page_id: The Shopify page ID.

    Returns:
        Dict with page fields: id, title, body_html, handle, published_at.
    """
    return _get_page(page_id)


def shopify_page_update(page_id: str, updates: dict) -> dict:
    """Update a Shopify page's content.

    Args:
        page_id: The Shopify page ID.
        updates: Fields to update (title, body_html, meta_title, meta_description).

    Returns:
        Dict with updated=True and the page_id.
    """
    page = _get_page_resource(page_id)
    for key, value in updates.items():
        setattr(page, key, value)
    page.save()
    return {"updated": True, "page_id": page_id, "fields_changed": list(updates.keys())}
```

**Step 4: Run tests to verify they pass**

Run: `pytest v5/vibe-inc/tests/test_shopify.py -v`
Expected: 4 passed

**Step 5: Commit**

```bash
git add v5/vibe-inc/tools/shopify.py v5/vibe-inc/tests/test_shopify.py
git commit -m "feat(vibe-inc): Shopify page read + update tools for CROps"
```

---

### Task 7: AdOps Operator — campaign_create

**Files:**
- Create: `v5/vibe-inc/roles/d2c_growth/ad_ops.py`
- Test: `v5/vibe-inc/tests/test_ad_ops.py`

**Step 1: Write failing tests**

```python
# v5/vibe-inc/tests/test_ad_ops.py
from openvibe_sdk.llm import LLMResponse, ToolCall


def _text_response(content="done"):
    return LLMResponse(content=content, stop_reason="end_turn")


def _tool_response(tool_name, tool_input=None):
    return LLMResponse(
        content="I'll use a tool.",
        tool_calls=[ToolCall(id="tc_1", name=tool_name, input=tool_input or {})],
        stop_reason="tool_use",
    )


class FakeAgentLLM:
    """Fake LLM that returns pre-configured responses in sequence."""
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def call(self, *, system, messages, **kwargs):
        self.calls.append({"system": system, "messages": messages, **kwargs})
        return self.responses.pop(0)


def test_campaign_create_is_agent_node():
    """campaign_create must be an agent_node with tools."""
    from vibe_inc.roles.d2c_growth.ad_ops import AdOps
    assert hasattr(AdOps.campaign_create, "_is_agent_node")
    assert AdOps.campaign_create._is_agent_node is True
    assert "meta_ads_create" in AdOps.campaign_create._node_config["tools"]


def test_campaign_create_uses_brief():
    """campaign_create sends the brief to the LLM."""
    from vibe_inc.roles.d2c_growth.ad_ops import AdOps

    llm = FakeAgentLLM([_text_response("Campaign created: Bot Foundation")])
    op = AdOps(llm=llm)
    result = op.campaign_create({"brief": {"product": "bot", "narrative": "foundation"}})

    assert result["campaign_result"] == "Campaign created: Bot Foundation"
    assert len(llm.calls) == 1
    assert "brief" in llm.calls[0]["messages"][-1]["content"]


def test_campaign_create_docstring_is_system_prompt():
    """The docstring becomes the LLM system prompt."""
    from vibe_inc.roles.d2c_growth.ad_ops import AdOps

    llm = FakeAgentLLM([_text_response()])
    op = AdOps(llm=llm)
    op.campaign_create({"brief": {}})

    assert "performance marketing" in llm.calls[0]["system"].lower()
```

**Step 2: Run test to verify it fails**

Run: `pytest v5/vibe-inc/tests/test_ad_ops.py -v`
Expected: FAIL

**Step 3: Implement AdOps.campaign_create**

```python
# v5/vibe-inc/roles/d2c_growth/ad_ops.py
"""AdOps operator — manages Meta and Google ad campaigns."""
from openvibe_sdk import Operator, agent_node

from vibe_inc.tools.meta_ads import meta_ads_read, meta_ads_create, meta_ads_update


class AdOps(Operator):
    operator_id = "ad_ops"

    @agent_node(
        tools=[meta_ads_read, meta_ads_create, meta_ads_update],
        output_key="campaign_result",
    )
    def campaign_create(self, state):
        """You are a performance marketing specialist for Vibe hardware products.

        Given a campaign brief, create a complete Meta Ads campaign structure:
        1. Review the brief (product, narrative, audience, budget).
        2. Read the messaging framework from shared memory for the product.
        3. Create a campaign with appropriate objective and naming convention:
           [Product] - [Narrative] - [Audience] - [Date]
        4. Use PAUSED status so human can review before activating.
        5. Always separate Net New audiences from Known (exclude site visitors, video viewers, prior clickers).

        Return a summary of what was created with IDs and configuration."""
        brief = state.get("brief", {})
        return f"Create campaign from brief: {brief}"
```

**Step 4: Run tests to verify they pass**

Run: `pytest v5/vibe-inc/tests/test_ad_ops.py -v`
Expected: 3 passed

**Step 5: Commit**

```bash
git add v5/vibe-inc/roles/d2c_growth/ad_ops.py v5/vibe-inc/tests/test_ad_ops.py
git commit -m "feat(vibe-inc): AdOps operator — campaign_create agent node"
```

---

### Task 8: AdOps Operator — daily_optimize

**Files:**
- Modify: `v5/vibe-inc/roles/d2c_growth/ad_ops.py`
- Test: `v5/vibe-inc/tests/test_ad_ops.py` (append)

**Step 1: Write failing tests**

```python
# Append to v5/vibe-inc/tests/test_ad_ops.py

def test_daily_optimize_is_agent_node():
    from vibe_inc.roles.d2c_growth.ad_ops import AdOps
    assert hasattr(AdOps.daily_optimize, "_is_agent_node")
    assert "meta_ads_read" in AdOps.daily_optimize._node_config["tools"]


def test_daily_optimize_reads_performance():
    from vibe_inc.roles.d2c_growth.ad_ops import AdOps

    llm = FakeAgentLLM([_text_response("Optimized: paused 2 underperformers")])
    op = AdOps(llm=llm)
    result = op.daily_optimize({"date": "2026-02-19"})

    assert "optimization_result" in result
    assert len(llm.calls) == 1


def test_daily_optimize_system_prompt_mentions_thresholds():
    from vibe_inc.roles.d2c_growth.ad_ops import AdOps

    llm = FakeAgentLLM([_text_response()])
    op = AdOps(llm=llm)
    op.daily_optimize({"date": "2026-02-19"})

    system = llm.calls[0]["system"]
    assert "20%" in system or "threshold" in system.lower()
```

**Step 2: Run test to verify it fails**

Run: `pytest v5/vibe-inc/tests/test_ad_ops.py::test_daily_optimize_is_agent_node -v`
Expected: FAIL

**Step 3: Add daily_optimize to AdOps**

```python
    # Add to AdOps class in ad_ops.py

    @agent_node(
        tools=[meta_ads_read, meta_ads_update],
        output_key="optimization_result",
    )
    def daily_optimize(self, state):
        """You are a performance marketing optimizer for Vibe hardware products.

        Review all active campaign performance from the last 24 hours:
        1. Read campaign-level and adset-level performance data.
        2. Compare CPA against target benchmarks (Bot: $400, Dot: $300).
        3. Apply these rules:
           - Bid adjustment ≤20%: execute autonomously.
           - Pause any ad with CPA >2x target: execute autonomously.
           - Budget change >$500/day: flag for approval (do not execute).
        4. Always calculate and report Net New CAC separately from Known.
        5. Summarize: what changed, what needs approval, overall health.

        Return a structured optimization report."""
        date = state.get("date", "today")
        return f"Review and optimize all active campaigns for {date}."
```

**Step 4: Run tests to verify they pass**

Run: `pytest v5/vibe-inc/tests/test_ad_ops.py -v`
Expected: 6 passed

**Step 5: Commit**

```bash
git add v5/vibe-inc/roles/d2c_growth/ad_ops.py v5/vibe-inc/tests/test_ad_ops.py
git commit -m "feat(vibe-inc): AdOps operator — daily_optimize with threshold rules"
```

---

### Task 9: AdOps Operator — weekly_report

**Files:**
- Modify: `v5/vibe-inc/roles/d2c_growth/ad_ops.py`
- Test: `v5/vibe-inc/tests/test_ad_ops.py` (append)

**Step 1: Write failing tests**

```python
# Append to v5/vibe-inc/tests/test_ad_ops.py

def test_weekly_report_is_agent_node():
    from vibe_inc.roles.d2c_growth.ad_ops import AdOps
    assert hasattr(AdOps.weekly_report, "_is_agent_node")


def test_weekly_report_output_key():
    from vibe_inc.roles.d2c_growth.ad_ops import AdOps

    llm = FakeAgentLLM([_text_response("Weekly: Bot CAC $380, Dot CAC $270")])
    op = AdOps(llm=llm)
    result = op.weekly_report({"week": "2026-W08"})

    assert "report" in result
```

**Step 2: Run test, verify fail, then implement**

Add to AdOps:

```python
    @agent_node(
        tools=[meta_ads_read],
        output_key="report",
    )
    def weekly_report(self, state):
        """You are a performance marketing analyst for Vibe.

        Generate a weekly performance report covering:
        1. Read all campaign data for the past 7 days.
        2. Calculate Net New CAC vs Known CAC by product (Bot, Dot, Board).
        3. Calculate ROAS by channel (Meta, Google).
        4. Report spend efficiency: revenue per visitor, cost per click.
        5. Highlight top 3 performers and bottom 3 underperformers.
        6. Compare against targets: Bot CAC ≤$400, Dot CAC ≤$300, CVR ≥2%.

        Format as progressive disclosure: headline → summary → detailed breakdown."""
        week = state.get("week", "current")
        return f"Generate weekly performance report for {week}."
```

**Step 3: Run tests, commit**

Run: `pytest v5/vibe-inc/tests/test_ad_ops.py -v`
Expected: 8 passed

```bash
git add v5/vibe-inc/roles/d2c_growth/ad_ops.py v5/vibe-inc/tests/test_ad_ops.py
git commit -m "feat(vibe-inc): AdOps operator — weekly_report with Net New vs Known CAC"
```

---

### Task 10: CROps Operator — experiment_analyze

**Files:**
- Create: `v5/vibe-inc/roles/d2c_growth/cro_ops.py`
- Test: `v5/vibe-inc/tests/test_cro_ops.py`

**Step 1: Write failing tests**

```python
# v5/vibe-inc/tests/test_cro_ops.py
from openvibe_sdk.llm import LLMResponse, ToolCall


def _text_response(content="done"):
    return LLMResponse(content=content, stop_reason="end_turn")


class FakeAgentLLM:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def call(self, *, system, messages, **kwargs):
        self.calls.append({"system": system, "messages": messages, **kwargs})
        return self.responses.pop(0)


def test_experiment_analyze_is_agent_node():
    from vibe_inc.roles.d2c_growth.cro_ops import CROps
    assert hasattr(CROps.experiment_analyze, "_is_agent_node")
    assert "ga4_read" in CROps.experiment_analyze._node_config["tools"]


def test_experiment_analyze_returns_analysis():
    from vibe_inc.roles.d2c_growth.cro_ops import CROps

    llm = FakeAgentLLM([_text_response("Foundation variant leads: CVR 2.1% vs 1.3% control")])
    op = CROps(llm=llm)
    result = op.experiment_analyze({"product": "bot"})

    assert "analysis" in result


def test_experiment_analyze_mentions_significance():
    from vibe_inc.roles.d2c_growth.cro_ops import CROps

    llm = FakeAgentLLM([_text_response()])
    op = CROps(llm=llm)
    op.experiment_analyze({"product": "bot"})

    system = llm.calls[0]["system"]
    assert "significance" in system.lower() or "confidence" in system.lower()
```

**Step 2: Implement CROps.experiment_analyze**

```python
# v5/vibe-inc/roles/d2c_growth/cro_ops.py
"""CROps operator — conversion rate optimization and experiment analysis."""
from openvibe_sdk import Operator, agent_node

from vibe_inc.tools.ga4 import ga4_read


class CROps(Operator):
    operator_id = "cro_ops"

    @agent_node(
        tools=[ga4_read],
        output_key="analysis",
    )
    def experiment_analyze(self, state):
        """You are a conversion rate optimization analyst for Vibe.

        Analyze the current story validation experiment:
        1. Read GA4 events for each PDP variant: pdp_view, scroll_depth, cta_click, begin_checkout, purchase.
        2. Calculate per-variant: scroll-to-CTA rate, CTA click rate, checkout initiation rate, CVR.
        3. Assess statistical significance (need >20,000 visitors per variant for reliable CVR).
        4. If sample size insufficient, report confidence level and recommend 'keep testing'.
        5. If significant winner found, recommend the winner with data backing.
        6. Compare against targets: scroll-to-CTA >70%, CTA click >2%, CVR ≥1%.

        Format: headline verdict → variant comparison table → detailed analysis."""
        product = state.get("product", "bot")
        return f"Analyze story validation experiment for {product} PDP variants."
```

**Step 3: Run tests, commit**

Run: `pytest v5/vibe-inc/tests/test_cro_ops.py -v`
Expected: 3 passed

```bash
git add v5/vibe-inc/roles/d2c_growth/cro_ops.py v5/vibe-inc/tests/test_cro_ops.py
git commit -m "feat(vibe-inc): CROps operator — experiment_analyze with significance checks"
```

---

### Task 11: CROps — funnel_diagnose

**Files:**
- Modify: `v5/vibe-inc/roles/d2c_growth/cro_ops.py`
- Test: `v5/vibe-inc/tests/test_cro_ops.py` (append)

**Step 1: Write tests, implement, run, commit**

```python
# Append to test_cro_ops.py

def test_funnel_diagnose_is_agent_node():
    from vibe_inc.roles.d2c_growth.cro_ops import CROps
    assert hasattr(CROps.funnel_diagnose, "_is_agent_node")


def test_funnel_diagnose_returns_diagnosis():
    from vibe_inc.roles.d2c_growth.cro_ops import CROps

    llm = FakeAgentLLM([_text_response("Biggest drop: checkout initiation (3.1% → 0.8%)")])
    op = CROps(llm=llm)
    result = op.funnel_diagnose({"product": "bot"})

    assert "diagnosis" in result
```

Add to CROps:

```python
    @agent_node(
        tools=[ga4_read],
        output_key="diagnosis",
    )
    def funnel_diagnose(self, state):
        """You are a funnel optimization analyst for Vibe.

        Diagnose the full D2C funnel for a product:
        1. Read GA4 data: sessions by source, page views, scroll depth, CTA clicks,
           add to cart, begin checkout, purchase — all by product.
        2. Calculate conversion rate between each stage.
        3. Identify the largest drop-off point (biggest % loss between stages).
        4. Recommend specific fixes for the top 3 drop-off points.
        5. Compare traffic quality by source (organic vs paid vs direct).

        Format: headline (biggest bottleneck) → funnel table → recommendations."""
        product = state.get("product", "bot")
        return f"Diagnose full funnel for {product}: impression → purchase."
```

Run: `pytest v5/vibe-inc/tests/test_cro_ops.py -v`
Expected: 5 passed

```bash
git add v5/vibe-inc/roles/d2c_growth/cro_ops.py v5/vibe-inc/tests/test_cro_ops.py
git commit -m "feat(vibe-inc): CROps operator — funnel_diagnose"
```

---

### Task 12: CROps — page_optimize

**Files:**
- Modify: `v5/vibe-inc/roles/d2c_growth/cro_ops.py`
- Test: `v5/vibe-inc/tests/test_cro_ops.py` (append)

**Step 1: Write tests**

```python
# Append to test_cro_ops.py

def test_page_optimize_is_agent_node():
    from vibe_inc.roles.d2c_growth.cro_ops import CROps
    assert hasattr(CROps.page_optimize, "_is_agent_node")
    tools = CROps.page_optimize._node_config["tools"]
    assert "shopify_page_read" in tools
    assert "shopify_page_update" in tools


def test_page_optimize_returns_result():
    from vibe_inc.roles.d2c_growth.cro_ops import CROps

    llm = FakeAgentLLM([_text_response("Updated headline: 'The room that remembers'")])
    op = CROps(llm=llm)
    result = op.page_optimize({
        "page_id": "123",
        "optimization": "headline",
        "rationale": "Foundation narrative winning in A/B test",
    })

    assert "optimization_result" in result


def test_page_optimize_mentions_approval():
    from vibe_inc.roles.d2c_growth.cro_ops import CROps

    llm = FakeAgentLLM([_text_response()])
    op = CROps(llm=llm)
    op.page_optimize({"page_id": "123", "optimization": "cta"})

    system = llm.calls[0]["system"]
    assert "approval" in system.lower() or "review" in system.lower()
```

**Step 2: Implement**

Add imports and method to CROps:

```python
from vibe_inc.tools.shopify import shopify_page_read, shopify_page_update

    # Add to CROps class (also add shopify imports at top)

    @agent_node(
        tools=[ga4_read, shopify_page_read, shopify_page_update],
        output_key="optimization_result",
    )
    def page_optimize(self, state):
        """You are a landing page optimization specialist for Vibe.

        Optimize a specific page element based on experiment data:
        1. Read the current page content from Shopify.
        2. Read the messaging framework for the product from shared memory.
        3. Generate an optimized version of the specified element (headline, CTA, body copy).
        4. Align with the winning narrative from story validation.
        5. Show before/after comparison for human review before applying.
        6. This change requires human approval — present the change clearly.

        Return: current content, proposed change, rationale, expected impact."""
        page_id = state.get("page_id")
        optimization = state.get("optimization", "headline")
        return f"Optimize {optimization} on page {page_id}. Read current content, propose improvement."
```

Run: `pytest v5/vibe-inc/tests/test_cro_ops.py -v`
Expected: 8 passed

```bash
git add v5/vibe-inc/roles/d2c_growth/cro_ops.py v5/vibe-inc/tests/test_cro_ops.py
git commit -m "feat(vibe-inc): CROps operator — page_optimize with Shopify integration"
```

---

### Task 13: D2CGrowth Role Class

**Files:**
- Modify: `v5/vibe-inc/roles/d2c_growth/__init__.py`
- Test: `v5/vibe-inc/tests/test_d2c_growth.py`

**Step 1: Write failing tests**

```python
# v5/vibe-inc/tests/test_d2c_growth.py
from openvibe_sdk.llm import LLMResponse


class FakeLLM:
    def __init__(self, content="ok"):
        self.content = content
        self.last_system = None
        self.calls = []

    def call(self, *, system, messages, **kwargs):
        self.last_system = system
        self.calls.append({"system": system, "messages": messages, **kwargs})
        return LLMResponse(content=self.content)


def test_d2c_growth_has_operators():
    from vibe_inc.roles.d2c_growth import D2CGrowth
    assert D2CGrowth.role_id == "d2c_growth"
    op_ids = [op.operator_id for op in D2CGrowth.operators]
    assert "ad_ops" in op_ids
    assert "cro_ops" in op_ids


def test_d2c_growth_has_soul():
    from vibe_inc.roles.d2c_growth import D2CGrowth
    assert D2CGrowth.soul != ""
    assert "Net New CAC" in D2CGrowth.soul


def test_d2c_growth_get_operator():
    from vibe_inc.roles.d2c_growth import D2CGrowth

    role = D2CGrowth(llm=FakeLLM())
    ad_ops = role.get_operator("ad_ops")
    assert ad_ops.operator_id == "ad_ops"


def test_d2c_growth_soul_injected_in_prompt():
    from vibe_inc.roles.d2c_growth import D2CGrowth

    llm = FakeLLM()
    role = D2CGrowth(llm=llm)
    ad_ops = role.get_operator("ad_ops")
    ad_ops.campaign_create({"brief": {"product": "bot"}})

    # Soul should be in the system prompt
    assert "Net New CAC" in llm.last_system
```

**Step 2: Run test, verify fail**

Run: `pytest v5/vibe-inc/tests/test_d2c_growth.py -v`
Expected: FAIL

**Step 3: Implement D2CGrowth**

```python
# v5/vibe-inc/roles/d2c_growth/__init__.py
"""D2C Growth role — manages paid acquisition and conversion optimization."""
from openvibe_sdk import Role

from .ad_ops import AdOps
from .cro_ops import CROps

_SOUL = """You are the D2C Growth for Vibe Inc.

Your mission: manage the full paid acquisition → landing page → conversion loop
for Vibe's hardware products (Bot, Dot, Board).

Core principles:
- Net New CAC is the only CAC that matters. Never report blended metrics.
- Separate Net New vs Known in every analysis and campaign.
- Story validation before scale — don't pour money into unvalidated narrative.
- Small bets, fast reads — $500 tests before $5K campaigns.
- Revenue per visitor > raw traffic volume.

You operate on daily data cycles. You are data-driven, capital-efficient,
and always questioning whether spend is reaching NEW customers.

Escalation rules:
- New campaign creation: require human approval.
- Budget change >$500/day: require human approval.
- Bid adjustment ≤20%: autonomous.
- Pause ad with CPA >2x target: autonomous.
- LP content change: require human approval.
"""


class D2CGrowth(Role):
    role_id = "d2c_growth"
    soul = _SOUL
    operators = [AdOps, CROps]
```

**Step 4: Run tests**

Run: `pytest v5/vibe-inc/tests/test_d2c_growth.py -v`
Expected: 4 passed

**Step 5: Commit**

```bash
git add v5/vibe-inc/roles/d2c_growth/__init__.py v5/vibe-inc/tests/test_d2c_growth.py
git commit -m "feat(vibe-inc): D2CGrowth role with soul + AdOps + CROps operators"
```

---

### Task 14: LangGraph Workflow Factories

**Files:**
- Create: `v5/vibe-inc/roles/d2c_growth/workflows.py`
- Test: `v5/vibe-inc/tests/test_workflows.py`

**Step 1: Write failing tests**

```python
# v5/vibe-inc/tests/test_workflows.py
from unittest.mock import MagicMock
from openvibe_sdk.llm import LLMResponse


class FakeLLM:
    def call(self, *, system, messages, **kwargs):
        return LLMResponse(content="done")


def test_daily_optimize_graph_compiles():
    from vibe_inc.roles.d2c_growth.workflows import create_daily_optimize_graph
    from vibe_inc.roles.d2c_growth.ad_ops import AdOps

    op = AdOps(llm=FakeLLM())
    graph = create_daily_optimize_graph(op)
    assert graph is not None


def test_daily_optimize_graph_invokes():
    from vibe_inc.roles.d2c_growth.workflows import create_daily_optimize_graph
    from vibe_inc.roles.d2c_growth.ad_ops import AdOps

    op = AdOps(llm=FakeLLM())
    graph = create_daily_optimize_graph(op)
    result = graph.invoke({"date": "2026-02-19"})
    assert "optimization_result" in result


def test_campaign_create_graph_compiles():
    from vibe_inc.roles.d2c_growth.workflows import create_campaign_create_graph
    from vibe_inc.roles.d2c_growth.ad_ops import AdOps

    op = AdOps(llm=FakeLLM())
    graph = create_campaign_create_graph(op)
    assert graph is not None


def test_experiment_analyze_graph_compiles():
    from vibe_inc.roles.d2c_growth.workflows import create_experiment_analyze_graph
    from vibe_inc.roles.d2c_growth.cro_ops import CROps

    op = CROps(llm=FakeLLM())
    graph = create_experiment_analyze_graph(op)
    assert graph is not None
```

**Step 2: Run test, verify fail**

**Step 3: Implement workflows.py**

```python
# v5/vibe-inc/roles/d2c_growth/workflows.py
"""LangGraph workflow factories for D2C Growth."""
from typing import TypedDict

from langgraph.graph import StateGraph


class OptimizeState(TypedDict, total=False):
    date: str
    optimization_result: str


class CampaignState(TypedDict, total=False):
    brief: dict
    campaign_result: str


class ExperimentState(TypedDict, total=False):
    product: str
    analysis: str


class FunnelState(TypedDict, total=False):
    product: str
    diagnosis: str


class PageOptimizeState(TypedDict, total=False):
    page_id: str
    optimization: str
    rationale: str
    optimization_result: str


class ReportState(TypedDict, total=False):
    week: str
    report: str


def create_daily_optimize_graph(operator):
    """Daily optimization: read performance → analyze → adjust bids."""
    graph = StateGraph(OptimizeState)
    graph.add_node("optimize", operator.daily_optimize)
    graph.set_entry_point("optimize")
    graph.set_finish_point("optimize")
    return graph.compile()


def create_campaign_create_graph(operator):
    """Campaign creation: read brief → build campaign → return IDs."""
    graph = StateGraph(CampaignState)
    graph.add_node("create", operator.campaign_create)
    graph.set_entry_point("create")
    graph.set_finish_point("create")
    return graph.compile()


def create_experiment_analyze_graph(operator):
    """Experiment analysis: read GA4 events → compute significance → recommend."""
    graph = StateGraph(ExperimentState)
    graph.add_node("analyze", operator.experiment_analyze)
    graph.set_entry_point("analyze")
    graph.set_finish_point("analyze")
    return graph.compile()


def create_funnel_diagnose_graph(operator):
    """Funnel diagnosis: read full funnel → identify drop-offs → recommend fixes."""
    graph = StateGraph(FunnelState)
    graph.add_node("diagnose", operator.funnel_diagnose)
    graph.set_entry_point("diagnose")
    graph.set_finish_point("diagnose")
    return graph.compile()


def create_page_optimize_graph(operator):
    """Page optimization: read page → propose change → apply (with approval)."""
    graph = StateGraph(PageOptimizeState)
    graph.add_node("optimize", operator.page_optimize)
    graph.set_entry_point("optimize")
    graph.set_finish_point("optimize")
    return graph.compile()


def create_weekly_report_graph(operator):
    """Weekly report: read all data → generate Net New vs Known report."""
    graph = StateGraph(ReportState)
    graph.add_node("report", operator.weekly_report)
    graph.set_entry_point("report")
    graph.set_finish_point("report")
    return graph.compile()
```

**Step 4: Run tests**

Run: `pytest v5/vibe-inc/tests/test_workflows.py -v`
Expected: 4 passed

**Step 5: Commit**

```bash
git add v5/vibe-inc/roles/d2c_growth/workflows.py v5/vibe-inc/tests/test_workflows.py
git commit -m "feat(vibe-inc): LangGraph workflow factories for all D2CGrowth workflows"
```

---

### Task 15: RoleRuntime Wiring + Activation

**Files:**
- Create: `v5/vibe-inc/main.py`
- Test: `v5/vibe-inc/tests/test_runtime_wiring.py`

**Step 1: Write failing tests**

```python
# v5/vibe-inc/tests/test_runtime_wiring.py
from openvibe_sdk.llm import LLMResponse


class FakeLLM:
    def call(self, *, system, messages, **kwargs):
        return LLMResponse(content="done")


def test_runtime_loads_d2c_growth():
    from vibe_inc.main import create_runtime

    runtime = create_runtime(llm=FakeLLM())
    role = runtime.get_role("d2c_growth")
    assert role.role_id == "d2c_growth"


def test_runtime_activates_daily_optimize():
    from vibe_inc.main import create_runtime

    runtime = create_runtime(llm=FakeLLM())
    result = runtime.activate(
        role_id="d2c_growth",
        operator_id="ad_ops",
        workflow_id="daily_optimize",
        input_data={"date": "2026-02-19"},
    )
    assert "optimization_result" in result


def test_runtime_activates_experiment_analyze():
    from vibe_inc.main import create_runtime

    runtime = create_runtime(llm=FakeLLM())
    result = runtime.activate(
        role_id="d2c_growth",
        operator_id="cro_ops",
        workflow_id="experiment_analyze",
        input_data={"product": "bot"},
    )
    assert "analysis" in result
```

**Step 2: Run test, verify fail**

**Step 3: Implement main.py**

```python
# v5/vibe-inc/main.py
"""Vibe Inc runtime — wires roles, operators, and workflows."""
from openvibe_sdk.llm import LLMProvider
from openvibe_sdk import RoleRuntime

from vibe_inc.roles.d2c_growth import D2CGrowth
from vibe_inc.roles.d2c_growth.workflows import (
    create_campaign_create_graph,
    create_daily_optimize_graph,
    create_experiment_analyze_graph,
    create_funnel_diagnose_graph,
    create_page_optimize_graph,
    create_weekly_report_graph,
)


def create_runtime(llm: LLMProvider) -> RoleRuntime:
    """Create and configure the Vibe Inc RoleRuntime.

    Registers all roles and workflow factories.
    """
    runtime = RoleRuntime(roles=[D2CGrowth], llm=llm)

    # AdOps workflows
    runtime.register_workflow("ad_ops", "campaign_create", create_campaign_create_graph)
    runtime.register_workflow("ad_ops", "daily_optimize", create_daily_optimize_graph)
    runtime.register_workflow("ad_ops", "weekly_report", create_weekly_report_graph)

    # CROps workflows
    runtime.register_workflow("cro_ops", "experiment_analyze", create_experiment_analyze_graph)
    runtime.register_workflow("cro_ops", "funnel_diagnose", create_funnel_diagnose_graph)
    runtime.register_workflow("cro_ops", "page_optimize", create_page_optimize_graph)

    return runtime
```

**Step 4: Run tests**

Run: `pytest v5/vibe-inc/tests/test_runtime_wiring.py -v`
Expected: 3 passed

**Step 5: Commit**

```bash
git add v5/vibe-inc/main.py v5/vibe-inc/tests/test_runtime_wiring.py
git commit -m "feat(vibe-inc): RoleRuntime wiring — all workflows registered"
```

---

### Task 16: Shared Memory Read/Write Helpers

**Files:**
- Create: `v5/vibe-inc/tools/shared_memory.py`
- Test: `v5/vibe-inc/tests/test_shared_memory_tools.py`

**Step 1: Write failing tests**

```python
# v5/vibe-inc/tests/test_shared_memory_tools.py
import tempfile
import yaml
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
```

**Step 2: Implement**

```python
# v5/vibe-inc/tools/shared_memory.py
"""Shared memory tools — YAML-based cross-role memory for Phase 1."""
from pathlib import Path
import yaml

_DEFAULT_MEMORY_DIR = Path(__file__).parent.parent / "shared_memory"


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
```

**Step 3: Run tests, commit**

Run: `pytest v5/vibe-inc/tests/test_shared_memory_tools.py -v`
Expected: 4 passed

```bash
git add v5/vibe-inc/tools/shared_memory.py v5/vibe-inc/tests/test_shared_memory_tools.py
git commit -m "feat(vibe-inc): shared memory YAML read/write tools"
```

---

### Task 17: Integration Test — Full Loop

**Files:**
- Create: `v5/vibe-inc/tests/test_integration.py`

**Step 1: Write integration test**

```python
# v5/vibe-inc/tests/test_integration.py
"""Integration test: full D2C Growth loop with FakeLLM."""
from openvibe_sdk.llm import LLMResponse


class FakeLLM:
    def call(self, *, system, messages, **kwargs):
        return LLMResponse(content="Integration test output")


def test_full_loop_daily_optimize_then_experiment_analyze():
    """Simulate a daily loop: AdOps optimize → CROps analyze."""
    from vibe_inc.main import create_runtime

    runtime = create_runtime(llm=FakeLLM())

    # Step 1: AdOps daily optimize
    opt_result = runtime.activate(
        role_id="d2c_growth",
        operator_id="ad_ops",
        workflow_id="daily_optimize",
        input_data={"date": "2026-02-19"},
    )
    assert "optimization_result" in opt_result

    # Step 2: CROps experiment analyze
    exp_result = runtime.activate(
        role_id="d2c_growth",
        operator_id="cro_ops",
        workflow_id="experiment_analyze",
        input_data={"product": "bot"},
    )
    assert "analysis" in exp_result


def test_full_loop_campaign_create():
    """Simulate campaign creation workflow."""
    from vibe_inc.main import create_runtime

    runtime = create_runtime(llm=FakeLLM())

    result = runtime.activate(
        role_id="d2c_growth",
        operator_id="ad_ops",
        workflow_id="campaign_create",
        input_data={"brief": {
            "product": "bot",
            "narrative": "foundation",
            "audience": "smb_managers",
            "budget_daily": 100,
        }},
    )
    assert "campaign_result" in result
```

**Step 2: Run tests**

Run: `pytest v5/vibe-inc/tests/test_integration.py -v`
Expected: 2 passed

**Step 3: Run ALL tests**

Run: `pytest v5/vibe-inc/tests/ -v`
Expected: ~51 passed

**Step 4: Commit**

```bash
git add v5/vibe-inc/tests/test_integration.py
git commit -m "test(vibe-inc): integration tests — full D2C Growth loop"
```

---

## Final Verification

Run the complete test suite:

```bash
# Vibe Inc tests
pytest v5/vibe-inc/tests/ -v

# Existing SDK tests still pass
pytest v5/openvibe-sdk/tests/ -v

# Existing runtime tests still pass
pytest v5/openvibe-runtime/tests/ -v

# Existing platform tests still pass
pytest v5/openvibe-platform/tests/ -v
```

Expected: All tests pass. No regressions.

```bash
git add -A && git commit -m "feat(vibe-inc): Phase 1 complete — D2C Growth role with AdOps + CROps"
```

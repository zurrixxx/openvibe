# Daily Growth Report Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a DailyReportOps operator to D2C Growth that queries Redshift for 3-layer business data and produces an interpreted daily growth report via Claude.

**Architecture:** Pre-written SQL queries fetch data from Redshift (deterministic), then a single @agent_node interprets the results using Ricky's 3-layer framework (L1 Business Outcomes → L2 Channel Efficiency → L3 Funnel Signal). Two-node LangGraph workflow: `fetch_data` (SQL) → `interpret` (Claude).

**Tech Stack:** Python 3.13, openvibe-sdk (Operator, agent_node), LangGraph (StateGraph), existing RedshiftProvider via analytics_query_sql.

**Design doc:** `v5/docs/plans/2026-02-24-daily-growth-report-design.md`

---

### Task 1: SQL Query Module — Tests

**Files:**
- Create: `v5/vibe-inc/tests/test_daily_report_queries.py`

**Step 1: Write failing tests for fetch_l1, fetch_l2, fetch_l3**

```python
"""Tests for daily_report_queries — verify SQL execution and result structure."""
from unittest.mock import patch, call


MOCK_ROWS = {"rows": [{"value": 1}], "columns": ["value"]}


def _patch_sql():
    return patch(
        "vibe_inc.roles.d2c_growth.daily_report_queries.analytics_query_sql",
        return_value=MOCK_ROWS,
    )


# --- fetch_l1 ---


def test_fetch_l1_returns_all_sections():
    from vibe_inc.roles.d2c_growth.daily_report_queries import fetch_l1

    with _patch_sql():
        result = fetch_l1("2026-02-23")

    assert "yesterday" in result
    assert "avg_7d" in result
    assert "avg_28d" in result
    assert "ad_spend" in result


def test_fetch_l1_queries_contain_fct_order():
    from vibe_inc.roles.d2c_growth.daily_report_queries import fetch_l1

    with _patch_sql() as mock_sql:
        fetch_l1("2026-02-23")

    sqls = [c.args[0] for c in mock_sql.call_args_list]
    assert len(sqls) == 4
    assert any("fct_order" in s for s in sqls[:3])
    assert any("fct_ads_ad_metrics" in s for s in sqls)


def test_fetch_l1_uses_provided_date():
    from vibe_inc.roles.d2c_growth.daily_report_queries import fetch_l1

    with _patch_sql() as mock_sql:
        fetch_l1("2026-01-15")

    sql_text = mock_sql.call_args_list[0].args[0]
    assert "2026-01-15" in sql_text


def test_fetch_l1_defaults_to_yesterday():
    from vibe_inc.roles.d2c_growth.daily_report_queries import fetch_l1

    with _patch_sql() as mock_sql:
        fetch_l1()

    sql_text = mock_sql.call_args_list[0].args[0]
    # Should contain a date string, not None
    assert "None" not in sql_text


# --- fetch_l2 ---


def test_fetch_l2_returns_all_sections():
    from vibe_inc.roles.d2c_growth.daily_report_queries import fetch_l2

    with _patch_sql():
        result = fetch_l2("2026-02-23")

    assert "yesterday" in result
    assert "avg_7d" in result
    assert "amazon" in result
    assert "top_campaigns" in result


def test_fetch_l2_queries_platform_and_amazon_tables():
    from vibe_inc.roles.d2c_growth.daily_report_queries import fetch_l2

    with _patch_sql() as mock_sql:
        fetch_l2("2026-02-23")

    sqls = [c.args[0] for c in mock_sql.call_args_list]
    assert any("fct_ads_ad_metrics" in s for s in sqls)
    assert any("fct_ads_amazon_ad_group_metrics" in s for s in sqls)
    assert any("dim_ads_campaign" in s for s in sqls)


# --- fetch_l3 ---


def test_fetch_l3_returns_all_sections():
    from vibe_inc.roles.d2c_growth.daily_report_queries import fetch_l3

    with _patch_sql():
        result = fetch_l3("2026-02-23")

    assert "sessions_yesterday" in result
    assert "sessions_7d" in result
    assert "funnel_yesterday" in result
    assert "funnel_7d" in result


def test_fetch_l3_queries_session_and_conversion_tables():
    from vibe_inc.roles.d2c_growth.daily_report_queries import fetch_l3

    with _patch_sql() as mock_sql:
        fetch_l3("2026-02-23")

    sqls = [c.args[0] for c in mock_sql.call_args_list]
    assert any("fct_website_session" in s for s in sqls)
    assert any("fct_website_visitor_conversion" in s for s in sqls)
```

**Step 2: Run tests to verify they fail**

Run: `cd v5/vibe-inc && python -m pytest tests/test_daily_report_queries.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'vibe_inc.roles.d2c_growth.daily_report_queries'`

**Step 3: Commit test file**

```bash
cd v5/vibe-inc
git add tests/test_daily_report_queries.py
git commit -m "test: add failing tests for daily report SQL queries"
```

---

### Task 2: SQL Query Module — Implementation

**Files:**
- Create: `v5/vibe-inc/src/vibe_inc/roles/d2c_growth/daily_report_queries.py`

**Step 1: Implement the module**

```python
"""SQL queries and data fetching for the Daily Growth Report.

Queries follow Ricky's 3-layer framework:
- L1: Business Outcomes (revenue, orders, CAC)
- L2: Channel Efficiency (per-platform spend, CPA)
- L3: Funnel Signal (traffic, conversion rates)

All queries are pre-written (deterministic). The LLM interprets results, not SQL.
"""

from datetime import UTC, datetime, timedelta

from vibe_inc.tools.analytics_tools import analytics_query_sql


def _yesterday() -> str:
    return (datetime.now(UTC) - timedelta(days=1)).strftime("%Y-%m-%d")


def _rolling_window(days: int, offset: int = 2) -> tuple[str, str]:
    """Return (start, end) for a rolling window ending `offset` days ago."""
    end = (datetime.now(UTC) - timedelta(days=offset)).strftime("%Y-%m-%d")
    start = (datetime.now(UTC) - timedelta(days=days + offset)).strftime("%Y-%m-%d")
    return start, end


def fetch_l1(date: str | None = None) -> dict:
    """L1 Business Outcomes: revenue by product, orders, ad spend for CAC."""
    d = date or _yesterday()
    start_7d, end_7d = _rolling_window(7)
    start_28d, end_28d = _rolling_window(28)

    revenue_yesterday = analytics_query_sql(
        f"SELECT DATE(created_at) as date,"
        f" SUM(board_net_sales) as board_revenue,"
        f" SUM(bot_net_sales) as bot_revenue,"
        f" SUM(net_sales) as total_revenue,"
        f" COUNT(*) as order_count"
        f" FROM common.fct_order"
        f" WHERE DATE(created_at) = '{d}'"
        f" GROUP BY 1"
    )

    revenue_7d = analytics_query_sql(
        f"SELECT"
        f" SUM(board_net_sales) / 7.0 as board_revenue_avg,"
        f" SUM(bot_net_sales) / 7.0 as bot_revenue_avg,"
        f" SUM(net_sales) / 7.0 as total_revenue_avg,"
        f" COUNT(*) / 7.0 as order_count_avg"
        f" FROM common.fct_order"
        f" WHERE DATE(created_at) BETWEEN '{start_7d}' AND '{end_7d}'"
    )

    revenue_28d = analytics_query_sql(
        f"SELECT"
        f" SUM(board_net_sales) / 28.0 as board_revenue_avg,"
        f" SUM(bot_net_sales) / 28.0 as bot_revenue_avg,"
        f" SUM(net_sales) / 28.0 as total_revenue_avg,"
        f" COUNT(*) / 28.0 as order_count_avg"
        f" FROM common.fct_order"
        f" WHERE DATE(created_at) BETWEEN '{start_28d}' AND '{end_28d}'"
    )

    ad_spend = analytics_query_sql(
        f"SELECT SUM(spend_in_usd) as total_spend"
        f" FROM common.fct_ads_ad_metrics"
        f" WHERE date = '{d}'"
    )

    return {
        "yesterday": revenue_yesterday.get("rows", []),
        "avg_7d": revenue_7d.get("rows", []),
        "avg_28d": revenue_28d.get("rows", []),
        "ad_spend": ad_spend.get("rows", []),
    }


def fetch_l2(date: str | None = None) -> dict:
    """L2 Channel Efficiency: per-platform metrics, Amazon, top campaigns."""
    d = date or _yesterday()
    start_7d, end_7d = _rolling_window(7)

    platform_yesterday = analytics_query_sql(
        f"SELECT platform,"
        f" SUM(spend_in_usd) as spend,"
        f" SUM(impressions) as impressions,"
        f" SUM(clicks) as clicks,"
        f" SUM(purchase_count) as purchases,"
        f" CASE WHEN SUM(purchase_count) > 0"
        f"   THEN SUM(spend_in_usd) / SUM(purchase_count)"
        f"   ELSE NULL END as cpa"
        f" FROM common.fct_ads_ad_metrics"
        f" WHERE date = '{d}'"
        f" GROUP BY platform"
    )

    platform_7d = analytics_query_sql(
        f"SELECT platform,"
        f" SUM(spend_in_usd) / 7.0 as spend_avg,"
        f" SUM(purchase_count) / 7.0 as purchases_avg,"
        f" CASE WHEN SUM(purchase_count) > 0"
        f"   THEN SUM(spend_in_usd) / SUM(purchase_count)"
        f"   ELSE NULL END as cpa_avg"
        f" FROM common.fct_ads_ad_metrics"
        f" WHERE date BETWEEN '{start_7d}' AND '{end_7d}'"
        f" GROUP BY platform"
    )

    amazon = analytics_query_sql(
        f"SELECT channel,"
        f" SUM(spend_in_usd) as spend,"
        f" SUM(impressions) as impressions,"
        f" SUM(clicks) as clicks,"
        f" SUM(conversions14d) as conversions,"
        f" SUM(sales14d) as sales,"
        f" CASE WHEN SUM(sales14d) > 0"
        f"   THEN SUM(spend_in_usd) / SUM(sales14d)"
        f"   ELSE NULL END as acos"
        f" FROM common.fct_ads_amazon_ad_group_metrics"
        f" WHERE date = '{d}'"
        f" GROUP BY channel"
    )

    top_campaigns = analytics_query_sql(
        f"SELECT c.campaign_name, f.platform,"
        f" SUM(f.spend_in_usd) as spend,"
        f" SUM(f.purchase_count) as purchases,"
        f" CASE WHEN SUM(f.purchase_count) > 0"
        f"   THEN SUM(f.spend_in_usd) / SUM(f.purchase_count)"
        f"   ELSE NULL END as cpa"
        f" FROM common.fct_ads_ad_metrics f"
        f" JOIN common.dim_ads_campaign c"
        f"   ON f.dim_ads_campaign_sk = c.dim_ads_campaign_sk"
        f" WHERE f.date = '{d}' AND f.spend_in_usd > 0"
        f" GROUP BY c.campaign_name, f.platform"
        f" ORDER BY cpa DESC LIMIT 10"
    )

    return {
        "yesterday": platform_yesterday.get("rows", []),
        "avg_7d": platform_7d.get("rows", []),
        "amazon": amazon.get("rows", []),
        "top_campaigns": top_campaigns.get("rows", []),
    }


def fetch_l3(date: str | None = None) -> dict:
    """L3 Funnel Signal: website sessions, conversion funnel, drop-offs."""
    d = date or _yesterday()
    start_7d, end_7d = _rolling_window(7)

    sessions_yesterday = analytics_query_sql(
        f"SELECT session_traffic_channel,"
        f" COUNT(*) as sessions,"
        f" AVG(session_page_viewed) as avg_pages,"
        f" AVG(session_time_engaged_in_s) as avg_time_s"
        f" FROM common.fct_website_session"
        f" WHERE DATE(session_first_page_tstamp) = '{d}'"
        f" GROUP BY session_traffic_channel"
    )

    sessions_7d = analytics_query_sql(
        f"SELECT session_traffic_channel,"
        f" COUNT(*) / 7.0 as sessions_avg"
        f" FROM common.fct_website_session"
        f" WHERE DATE(session_first_page_tstamp) BETWEEN '{start_7d}' AND '{end_7d}'"
        f" GROUP BY session_traffic_channel"
    )

    funnel_yesterday = analytics_query_sql(
        f"SELECT conversion,"
        f" COUNT(*) as count,"
        f" SUM(conversion_value) as value"
        f" FROM common.fct_website_visitor_conversion"
        f" WHERE DATE(original_tstamp) = '{d}'"
        f" GROUP BY conversion"
    )

    funnel_7d = analytics_query_sql(
        f"SELECT conversion,"
        f" COUNT(*) / 7.0 as count_avg,"
        f" SUM(conversion_value) / 7.0 as value_avg"
        f" FROM common.fct_website_visitor_conversion"
        f" WHERE DATE(original_tstamp) BETWEEN '{start_7d}' AND '{end_7d}'"
        f" GROUP BY conversion"
    )

    return {
        "sessions_yesterday": sessions_yesterday.get("rows", []),
        "sessions_7d": sessions_7d.get("rows", []),
        "funnel_yesterday": funnel_yesterday.get("rows", []),
        "funnel_7d": funnel_7d.get("rows", []),
    }
```

**Step 2: Run tests to verify they pass**

Run: `cd v5/vibe-inc && python -m pytest tests/test_daily_report_queries.py -v`
Expected: 8 tests PASS

**Step 3: Commit**

```bash
cd v5/vibe-inc
git add src/vibe_inc/roles/d2c_growth/daily_report_queries.py
git commit -m "feat(daily-report): add SQL query module for 3-layer data fetching"
```

---

### Task 3: DailyReportOps Operator — Tests

**Files:**
- Create: `v5/vibe-inc/tests/test_daily_report_ops.py`

**Step 1: Write failing tests**

```python
"""Tests for DailyReportOps operator."""
from unittest.mock import patch

from openvibe_sdk.llm import LLMResponse


MOCK_L1 = {"yesterday": [{"total_revenue": 15000}], "avg_7d": [], "avg_28d": [], "ad_spend": []}
MOCK_L2 = {"yesterday": [], "avg_7d": [], "amazon": [], "top_campaigns": []}
MOCK_L3 = {"sessions_yesterday": [], "sessions_7d": [], "funnel_yesterday": [], "funnel_7d": []}


def _text_response(content="done"):
    return LLMResponse(content=content, stop_reason="end_turn")


class FakeAgentLLM:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def call(self, *, system, messages, **kwargs):
        self.calls.append({"system": system, "messages": messages, **kwargs})
        return self.responses.pop(0)


# --- interpret ---


def test_interpret_is_agent_node():
    from vibe_inc.roles.d2c_growth.daily_report_ops import DailyReportOps

    assert hasattr(DailyReportOps.interpret, "_is_agent_node")
    assert DailyReportOps.interpret._is_agent_node is True
    assert "read_memory" in DailyReportOps.interpret._node_config["tools"]


def test_interpret_output_key():
    from vibe_inc.roles.d2c_growth.daily_report_ops import DailyReportOps

    llm = FakeAgentLLM([_text_response("🔴 Bot CAC $520...")])
    op = DailyReportOps(llm=llm)
    result = op.interpret({"l1_data": MOCK_L1, "l2_data": MOCK_L2, "l3_data": MOCK_L3})

    assert "report" in result
    assert "Bot CAC" in result["report"]


def test_interpret_prompt_contains_framework_keywords():
    from vibe_inc.roles.d2c_growth.daily_report_ops import DailyReportOps

    llm = FakeAgentLLM([_text_response("report")])
    op = DailyReportOps(llm=llm)
    op.interpret({"l1_data": MOCK_L1, "l2_data": MOCK_L2, "l3_data": MOCK_L3})

    system_prompt = llm.calls[0]["system"].lower()
    assert "net new cac" in system_prompt
    assert "benchmark" in system_prompt


def test_interpret_user_message_contains_data():
    from vibe_inc.roles.d2c_growth.daily_report_ops import DailyReportOps

    llm = FakeAgentLLM([_text_response("report")])
    op = DailyReportOps(llm=llm)
    op.interpret({"l1_data": MOCK_L1, "l2_data": MOCK_L2, "l3_data": MOCK_L3})

    user_msg = llm.calls[0]["messages"][-1]["content"].lower()
    assert "l1" in user_msg
    assert "l2" in user_msg
    assert "l3" in user_msg


# --- fetch_data ---


def test_fetch_data_calls_all_three_layers():
    from vibe_inc.roles.d2c_growth.daily_report_ops import DailyReportOps

    with patch("vibe_inc.roles.d2c_growth.daily_report_ops.fetch_l1", return_value=MOCK_L1) as m1, \
         patch("vibe_inc.roles.d2c_growth.daily_report_ops.fetch_l2", return_value=MOCK_L2) as m2, \
         patch("vibe_inc.roles.d2c_growth.daily_report_ops.fetch_l3", return_value=MOCK_L3) as m3:
        llm = FakeAgentLLM([])
        op = DailyReportOps(llm=llm)
        result = op.fetch_data({"date": "2026-02-23"})

    m1.assert_called_once_with("2026-02-23")
    m2.assert_called_once_with("2026-02-23")
    m3.assert_called_once_with("2026-02-23")
    assert result["l1_data"] == MOCK_L1
    assert result["l2_data"] == MOCK_L2
    assert result["l3_data"] == MOCK_L3


def test_fetch_data_passes_none_when_no_date():
    from vibe_inc.roles.d2c_growth.daily_report_ops import DailyReportOps

    with patch("vibe_inc.roles.d2c_growth.daily_report_ops.fetch_l1", return_value=MOCK_L1), \
         patch("vibe_inc.roles.d2c_growth.daily_report_ops.fetch_l2", return_value=MOCK_L2), \
         patch("vibe_inc.roles.d2c_growth.daily_report_ops.fetch_l3", return_value=MOCK_L3):
        llm = FakeAgentLLM([])
        op = DailyReportOps(llm=llm)
        result = op.fetch_data({})

    assert "l1_data" in result
    assert "l2_data" in result
    assert "l3_data" in result
```

**Step 2: Run tests to verify they fail**

Run: `cd v5/vibe-inc && python -m pytest tests/test_daily_report_ops.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'vibe_inc.roles.d2c_growth.daily_report_ops'`

**Step 3: Commit test file**

```bash
cd v5/vibe-inc
git add tests/test_daily_report_ops.py
git commit -m "test: add failing tests for DailyReportOps operator"
```

---

### Task 4: DailyReportOps Operator — Implementation

**Files:**
- Create: `v5/vibe-inc/src/vibe_inc/roles/d2c_growth/daily_report_ops.py`

**Step 1: Implement the operator**

```python
"""DailyReportOps operator — daily growth report from Redshift data."""

import json

from openvibe_sdk import Operator, agent_node

from vibe_inc.tools.shared_memory import read_memory

from .daily_report_queries import fetch_l1, fetch_l2, fetch_l3


class DailyReportOps(Operator):
    operator_id = "daily_report_ops"

    def fetch_data(self, state):
        """Deterministic data fetching — runs pre-written SQL against Redshift."""
        date = state.get("date")
        return {
            "l1_data": fetch_l1(date),
            "l2_data": fetch_l2(date),
            "l3_data": fetch_l3(date),
        }

    @agent_node(
        tools=[read_memory],
        output_key="report",
    )
    def interpret(self, state):
        """You are a D2C growth analyst for Vibe hardware products (Board, Bot, Dot).

        You receive three layers of pre-queried Redshift data:
        - L1: business outcomes (revenue, orders, CAC by product)
        - L2: channel efficiency (per-platform spend, CPA, trends)
        - L3: funnel signal (traffic, conversion rates, drop-offs)

        Produce a Daily Growth Report in this exact structure:

        1. HEADLINE — one sentence: single most important thing today.
           Flag: 🔴 (action needed), ⚠️ (watch), ✅ (all clear).
           Red if: any L1 metric >20% off target OR any platform CPA >1.5x target.
           Yellow if: any L1 metric >10% off OR trending wrong 3+ days.
           Green if: all within targets and stable.

        2. L1 TABLE — revenue + CAC by product, columns: Yesterday | 7d Avg | 28d Avg | Target.

        3. L2 TABLE — per-platform: Spend | CPA | vs Target | vs 7d Avg | Flag.
           Include Amazon ACOS separately.
           List top campaigns by worst CPA for actionability.

        4. L3 TABLE — traffic by channel and funnel steps with conversion rates vs 7d avg.

        5. RECOMMENDED ACTIONS — numbered, specific, with expected impact.
           Format: [PLATFORM] verb + specific target + reason + expected impact.

        Rules:
        - Net New CAC is the only CAC that matters. If the data does not separate
          Net New vs Known, flag this as a measurement gap in the headline.
        - Never say "optimize" without saying what specifically to do.
        - Classify anomalies: structural (trend 3+ days) vs noise (single day).
        - If data is missing or empty, say so. Do not fabricate numbers.
        - Benchmarks: Bot CAC ≤$400, Dot CAC ≤$300, Board ACOS ≤20%.
        - Use read_memory("performance/cac-benchmarks") and
          read_memory("performance/platform_benchmarks") for exact thresholds.
        - Every number must have context: vs target, vs 7d avg, or vs 28d avg."""
        l1 = json.dumps(state.get("l1_data", {}), indent=2, default=str)
        l2 = json.dumps(state.get("l2_data", {}), indent=2, default=str)
        l3 = json.dumps(state.get("l3_data", {}), indent=2, default=str)
        date = state.get("date", "yesterday")
        return (
            f"Generate the Daily Growth Report for {date}.\n\n"
            f"L1 (Business Outcomes):\n{l1}\n\n"
            f"L2 (Channel Efficiency):\n{l2}\n\n"
            f"L3 (Funnel Signal):\n{l3}"
        )
```

**Step 2: Run tests to verify they pass**

Run: `cd v5/vibe-inc && python -m pytest tests/test_daily_report_ops.py -v`
Expected: 6 tests PASS

**Step 3: Commit**

```bash
cd v5/vibe-inc
git add src/vibe_inc/roles/d2c_growth/daily_report_ops.py
git commit -m "feat(daily-report): add DailyReportOps operator — fetch + interpret"
```

---

### Task 5: Workflow — Tests

**Files:**
- Create: `v5/vibe-inc/tests/test_daily_report_workflows.py`

**Step 1: Write failing tests**

```python
"""Tests for daily report workflow graph."""
from unittest.mock import patch

from openvibe_sdk.llm import LLMResponse


MOCK_L1 = {"yesterday": [], "avg_7d": [], "avg_28d": [], "ad_spend": []}
MOCK_L2 = {"yesterday": [], "avg_7d": [], "amazon": [], "top_campaigns": []}
MOCK_L3 = {"sessions_yesterday": [], "sessions_7d": [], "funnel_yesterday": [], "funnel_7d": []}


class FakeLLM:
    def call(self, *, system, messages, **kwargs):
        return LLMResponse(content="✅ All metrics healthy.")


def test_daily_growth_report_graph_compiles():
    from vibe_inc.roles.d2c_growth.daily_report_workflows import create_daily_growth_report_graph
    from vibe_inc.roles.d2c_growth.daily_report_ops import DailyReportOps

    op = DailyReportOps(llm=FakeLLM())
    graph = create_daily_growth_report_graph(op)
    assert graph is not None


def test_daily_growth_report_graph_invokes_end_to_end():
    from vibe_inc.roles.d2c_growth.daily_report_workflows import create_daily_growth_report_graph
    from vibe_inc.roles.d2c_growth.daily_report_ops import DailyReportOps

    op = DailyReportOps(llm=FakeLLM())
    graph = create_daily_growth_report_graph(op)

    with patch("vibe_inc.roles.d2c_growth.daily_report_queries.analytics_query_sql",
               return_value={"rows": [], "columns": []}):
        result = graph.invoke({"date": "2026-02-23"})

    assert "report" in result
    assert "healthy" in result["report"].lower()


def test_daily_growth_report_state_contains_layer_data():
    from vibe_inc.roles.d2c_growth.daily_report_workflows import create_daily_growth_report_graph
    from vibe_inc.roles.d2c_growth.daily_report_ops import DailyReportOps

    op = DailyReportOps(llm=FakeLLM())
    graph = create_daily_growth_report_graph(op)

    with patch("vibe_inc.roles.d2c_growth.daily_report_queries.analytics_query_sql",
               return_value={"rows": [{"x": 1}], "columns": ["x"]}):
        result = graph.invoke({"date": "2026-02-23"})

    assert "l1_data" in result
    assert "l2_data" in result
    assert "l3_data" in result
```

**Step 2: Run tests to verify they fail**

Run: `cd v5/vibe-inc && python -m pytest tests/test_daily_report_workflows.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'vibe_inc.roles.d2c_growth.daily_report_workflows'`

**Step 3: Commit test file**

```bash
cd v5/vibe-inc
git add tests/test_daily_report_workflows.py
git commit -m "test: add failing tests for daily report workflow graph"
```

---

### Task 6: Workflow — Implementation

**Files:**
- Create: `v5/vibe-inc/src/vibe_inc/roles/d2c_growth/daily_report_workflows.py`

**Step 1: Implement the workflow**

```python
"""LangGraph workflow factory for DailyReportOps."""

from typing import TypedDict

from langgraph.graph import StateGraph


class DailyReportState(TypedDict, total=False):
    date: str
    l1_data: dict
    l2_data: dict
    l3_data: dict
    report: str


def create_daily_growth_report_graph(operator):
    """Daily growth report: fetch Redshift data → interpret with Claude.

    Two nodes:
    - fetch_data: deterministic SQL execution for L1/L2/L3
    - interpret: Claude analyzes data and produces formatted report
    """
    graph = StateGraph(DailyReportState)
    graph.add_node("fetch_data", operator.fetch_data)
    graph.add_node("interpret", operator.interpret)
    graph.add_edge("fetch_data", "interpret")
    graph.set_entry_point("fetch_data")
    graph.set_finish_point("interpret")
    return graph.compile()
```

**Step 2: Run tests to verify they pass**

Run: `cd v5/vibe-inc && python -m pytest tests/test_daily_report_workflows.py -v`
Expected: 3 tests PASS

**Step 3: Commit**

```bash
cd v5/vibe-inc
git add src/vibe_inc/roles/d2c_growth/daily_report_workflows.py
git commit -m "feat(daily-report): add workflow graph — fetch_data → interpret"
```

---

### Task 7: Register Operator + Full Test Suite

**Files:**
- Modify: `v5/vibe-inc/src/vibe_inc/roles/d2c_growth/__init__.py`

**Step 1: Add DailyReportOps to imports and operator list**

Add import after existing imports:
```python
from .daily_report_ops import DailyReportOps
```

Add `DailyReportOps` to the `operators` list in `D2CGrowth`:
```python
    operators = [
        MetaAdOps, GoogleAdOps, AmazonAdOps, TikTokAdOps,
        LinkedInAdOps, PinterestAdOps, EmailOps, CROps,
        CrossPlatformOps,
        CRMOps,
        DailyReportOps,
    ]
```

**Step 2: Run ALL vibe-inc tests**

Run: `cd v5/vibe-inc && python -m pytest tests/ -v`
Expected: 384 tests PASS (367 existing + 17 new: 8 queries + 6 ops + 3 workflows)

**Step 3: Run SDK tests to verify no regressions**

Run: `cd v5/openvibe-sdk && python -m pytest tests/ -v`
Expected: 279 tests PASS

**Step 4: Commit**

```bash
cd v5/vibe-inc
git add src/vibe_inc/roles/d2c_growth/__init__.py
git commit -m "feat(daily-report): register DailyReportOps in D2C Growth — 11th operator"
```

---

## Summary

| Task | What | Files | Tests |
|------|------|-------|-------|
| 1-2 | SQL query module | daily_report_queries.py | 8 |
| 3-4 | Operator | daily_report_ops.py | 6 |
| 5-6 | Workflow | daily_report_workflows.py | 3 |
| 7 | Register + verify | __init__.py | — |
| **Total** | | **3 new files, 1 modified** | **17 new tests** |

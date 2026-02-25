"""Tests for daily_report_queries — verify SQL execution and result structure."""
from unittest.mock import patch


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
    assert "worst_cpa_campaigns" in result


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

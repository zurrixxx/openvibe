"""SQL queries and data fetching for the Daily Growth Report.

Queries follow Ricky's 3-layer framework:
- L1: Business Outcomes (revenue, orders, CAC)
- L2: Channel Efficiency (per-platform spend, CPA)
- L3: Funnel Signal (traffic, conversion rates)

All queries are pre-written (deterministic). The LLM interprets results, not SQL.
"""

import re
from datetime import UTC, datetime, timedelta

from vibe_inc.tools.analytics_tools import analytics_query_sql

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _yesterday() -> str:
    return (datetime.now(UTC) - timedelta(days=1)).strftime("%Y-%m-%d")


def _rolling_window(days: int, offset: int = 2) -> tuple[str, str]:
    """Return (start, end) for a rolling window ending `offset` days ago.

    Default offset=2 accounts for Redshift data pipeline lag (T-2 availability).
    """
    now = datetime.now(UTC)
    end = (now - timedelta(days=offset)).strftime("%Y-%m-%d")
    start = (now - timedelta(days=days + offset)).strftime("%Y-%m-%d")
    return start, end


def _safe_date(date: str | None) -> str:
    """Validate and return a YYYY-MM-DD date string."""
    d = date or _yesterday()
    if not _DATE_RE.match(d):
        raise ValueError(f"Invalid date format: {d!r}")
    return d


def fetch_l1(date: str | None = None) -> dict:
    """L1 Business Outcomes: revenue by product, orders, ad spend for CAC."""
    d = _safe_date(date)
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
    d = _safe_date(date)
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
        f" ORDER BY cpa DESC NULLS LAST LIMIT 10"
    )

    return {
        "yesterday": platform_yesterday.get("rows", []),
        "avg_7d": platform_7d.get("rows", []),
        "amazon": amazon.get("rows", []),
        "worst_cpa_campaigns": top_campaigns.get("rows", []),
    }


def fetch_l3(date: str | None = None) -> dict:
    """L3 Funnel Signal: website sessions, conversion funnel, drop-offs."""
    d = _safe_date(date)
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

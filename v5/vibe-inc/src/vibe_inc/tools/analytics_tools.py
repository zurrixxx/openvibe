"""Analytics tool functions — exposed to all operators via @agent_node(tools=[...]).

Default provider: RedshiftProvider (queries dbt-materialized tables in Redshift).
Secondary: MixpanelProvider (real-time), GA4Provider (real-time traffic).
"""
from vibe_inc.tools.analytics.redshift import RedshiftProvider


def _get_provider():
    """Get the default analytics provider (Redshift — primary data source)."""
    return RedshiftProvider()


def analytics_query_metrics(
    metrics: list[str],
    dimensions: list[str] | None = None,
    date_range: str = "last_7d",
    filters: dict | None = None,
) -> dict:
    """Query aggregated metrics from the data warehouse (Redshift via dbt).

    Args:
        metrics: Metric column names (e.g. spend_in_usd, impressions, net_sales).
        dimensions: Optional dimension breakdowns (e.g. platform, campaign_name).
        date_range: Date range — last_7d, last_28d, last_90d, or YYYY-MM-DD,YYYY-MM-DD.
        filters: Optional filters as dict (e.g. {"platform": "facebook"}).

    Returns:
        Dict with 'rows' (list of dicts) and 'date_range'.
    """
    return _get_provider().query_metrics(metrics, dimensions, date_range, filters)


def analytics_query_funnel(
    steps: list[str],
    date_range: str = "last_7d",
    filters: dict | None = None,
) -> dict:
    """Query funnel drop-off analysis from website conversion events.

    Args:
        steps: Ordered list of conversion names (e.g. visitor_add_to_cart,
               visitor_init_checkout, visitor_close_won).
        date_range: Date range.
        filters: Optional filters.

    Returns:
        Dict with funnel data including per-step counts.
    """
    return _get_provider().query_funnel(steps, date_range, filters)


def analytics_query_events(
    event_name: str,
    date_range: str = "last_7d",
    properties: list[str] | None = None,
    filters: dict | None = None,
) -> dict:
    """Query raw conversion events from the data warehouse.

    Args:
        event_name: Conversion event name (e.g. visitor_close_won).
        date_range: Date range.
        properties: Additional columns to include.
        filters: Optional filters.

    Returns:
        Dict with 'events' list.
    """
    return _get_provider().query_events(event_name, date_range, properties, filters)


def analytics_query_cohort(
    cohort_property: str,
    metric: str,
    date_range: str = "last_90d",
) -> dict:
    """Query cohort analysis from the data warehouse.

    Args:
        cohort_property: Date column to define cohorts (e.g. created_at).
        metric: Metric to aggregate (e.g. net_sales).
        date_range: Date range.

    Returns:
        Dict with cohort data.
    """
    return _get_provider().query_cohort(cohort_property, metric, date_range)


def analytics_query_sql(sql: str) -> dict:
    """Execute raw SQL against the Redshift data warehouse.

    Args:
        sql: SQL query string.

    Returns:
        Dict with 'rows' and 'columns'.
    """
    return _get_provider().query_sql(sql)

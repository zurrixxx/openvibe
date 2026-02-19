"""Redshift analytics provider — primary data access via dbt-materialized tables.

Reads the curated dbt catalog (shared_memory/data/catalog.yaml) to understand
available tables and columns. Generates dynamic SQL for all query methods.
"""
import os
from datetime import UTC, datetime, timedelta
from pathlib import Path

import yaml


_CATALOG_PATH = Path(__file__).resolve().parents[4] / "shared_memory" / "data" / "catalog.yaml"

# Columns that live on dimension tables, requiring a JOIN
_DIM_COLUMNS = {
    "campaign_name": ("dim_ads_campaign", "dim_ads_campaign_sk"),
    "account_name": ("dim_ads_campaign", "dim_ads_campaign_sk"),
    "ad_group_name": ("dim_ads_ad_group", "dim_ads_ad_group_sk"),
    "ad_name": ("dim_ads_ad", "dim_ads_ad_sk"),
}


def _get_connection():
    """Get a Redshift connection from environment variables."""
    import redshift_connector
    return redshift_connector.connect(
        host=os.environ.get("REDSHIFT_HOST", ""),
        port=int(os.environ.get("REDSHIFT_PORT", "5439")),
        database=os.environ.get("REDSHIFT_DATABASE", ""),
        user=os.environ.get("REDSHIFT_USER", ""),
        password=os.environ.get("REDSHIFT_PASSWORD", ""),
    )


def _parse_date_range(date_range: str) -> tuple[str, str]:
    """Convert date_range string to (start, end) in YYYY-MM-DD."""
    if "," in date_range:
        parts = date_range.split(",", 1)
        return parts[0].strip(), parts[1].strip()
    days = {"last_7d": 7, "last_28d": 28, "last_90d": 90, "last_24h": 1}
    n = days.get(date_range, 7)
    end = datetime.now(UTC).strftime("%Y-%m-%d")
    start = (datetime.now(UTC) - timedelta(days=n)).strftime("%Y-%m-%d")
    return start, end


def _execute(conn, sql: str) -> dict:
    """Execute SQL and return rows as list of dicts."""
    cursor = conn.cursor()
    cursor.execute(sql)
    if cursor.description is None:
        return {"rows": [], "columns": []}
    columns = [desc[0] for desc in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return {"rows": rows, "columns": columns}


def _resolve_table(catalog: dict, columns: list[str]) -> str:
    """Find the best fact table for the given metric columns."""
    # Priority order for metric resolution
    metric_indicators = {
        "fct_ads_ad_metrics": ["spend_in_usd", "spend_in_lcy", "impressions", "clicks", "purchase_count"],
        "fct_order": ["net_sales", "total_price", "subtotal_price", "board_net_sales", "bot_net_sales"],
        "fct_website_session": ["session_page_viewed", "session_time_engaged_in_s", "session_traffic_channel"],
        "fct_website_visitor_conversion": ["conversion", "conversion_value"],
        "fct_email_event": ["count_open_total", "count_click_total", "sent_result"],
    }
    for table_name, indicators in metric_indicators.items():
        if any(col in indicators for col in columns):
            table_def = next((t for t in catalog["tables"] if t["name"] == table_name), None)
            if table_def:
                return f'{table_def["schema"]}.{table_name}'
    # Default to ads metrics
    return "common.fct_ads_ad_metrics"


def _get_date_column(table_ref: str) -> str:
    """Get the date column name for a table."""
    date_cols = {
        "fct_ads_ad_metrics": "date",
        "fct_order": "created_at",
        "fct_website_session": "session_first_page_tstamp",
        "fct_website_visitor_conversion": "original_tstamp",
        "fct_email_event": "sent_tstamp",
    }
    table_name = table_ref.split(".")[-1]
    return date_cols.get(table_name, "date")


class RedshiftProvider:
    """Redshift analytics provider — primary data access layer.

    Reads the dbt catalog to understand schema. Generates SQL dynamically.
    All other providers (Mixpanel, GA4) are secondary/real-time fallbacks.
    """

    def __init__(self, catalog_path: Path | None = None):
        path = catalog_path or _CATALOG_PATH
        self.catalog = yaml.safe_load(path.read_text())

    def query_metrics(
        self,
        metrics: list[str],
        dimensions: list[str] | None = None,
        date_range: str = "last_7d",
        filters: dict | None = None,
    ) -> dict:
        dims = dimensions or []
        all_cols = metrics + dims
        table_ref = _resolve_table(self.catalog, all_cols)
        date_col = _get_date_column(table_ref)
        start, end = _parse_date_range(date_range)

        # Check if any dimension columns require JOIN
        joins = []
        select_dims = []
        for d in dims:
            if d in _DIM_COLUMNS:
                dim_table, join_key = _DIM_COLUMNS[d]
                dim_schema = next(
                    (t["schema"] for t in self.catalog["tables"] if t["name"] == dim_table),
                    "common",
                )
                alias = dim_table.replace("dim_", "d_")
                joins.append(f"JOIN {dim_schema}.{dim_table} {alias} ON f.{join_key} = {alias}.{join_key}")
                select_dims.append(f"{alias}.{d}")
            else:
                select_dims.append(f"f.{d}")

        select_metrics = [f"SUM(f.{m}) as {m}" if m not in dims else f"f.{m}" for m in metrics]
        select_clause = ", ".join(select_dims + select_metrics)
        join_clause = " ".join(joins)
        group_clause = f"GROUP BY {', '.join(select_dims)}" if dims else ""

        # Build filter clause
        filter_parts = [f"f.{date_col} >= '{start}' AND f.{date_col} <= '{end}'"]
        if filters:
            for k, v in filters.items():
                if isinstance(v, list):
                    vals = ", ".join(f"'{x}'" for x in v)
                    filter_parts.append(f"f.{k} IN ({vals})")
                else:
                    filter_parts.append(f"f.{k} = '{v}'")
        where_clause = " AND ".join(filter_parts)

        sql = f"SELECT {select_clause} FROM {table_ref} f {join_clause} WHERE {where_clause} {group_clause}"

        conn = _get_connection()
        try:
            result = _execute(conn, sql)
            return {"rows": result["rows"], "date_range": date_range, "sql": sql}
        finally:
            conn.close()

    def query_funnel(
        self,
        steps: list[str],
        date_range: str = "last_7d",
        filters: dict | None = None,
    ) -> dict:
        start, end = _parse_date_range(date_range)
        step_list = ", ".join(f"'{s}'" for s in steps)
        sql = (
            f"SELECT conversion, COUNT(*) as count "
            f"FROM common.fct_website_visitor_conversion "
            f"WHERE conversion IN ({step_list}) "
            f"AND original_tstamp >= '{start}' AND original_tstamp <= '{end}' "
            f"GROUP BY conversion "
            f"ORDER BY COUNT(*) DESC"
        )

        conn = _get_connection()
        try:
            result = _execute(conn, sql)
            return {"data": result["rows"], "steps": steps, "date_range": date_range, "sql": sql}
        finally:
            conn.close()

    def query_events(
        self,
        event_name: str,
        date_range: str = "last_7d",
        properties: list[str] | None = None,
        filters: dict | None = None,
    ) -> dict:
        start, end = _parse_date_range(date_range)
        cols = ["conversion", "conversion_value", "detail", "original_tstamp"]
        if properties:
            cols.extend(properties)
        select_clause = ", ".join(cols)
        sql = (
            f"SELECT {select_clause} "
            f"FROM common.fct_website_visitor_conversion "
            f"WHERE conversion = '{event_name}' "
            f"AND original_tstamp >= '{start}' AND original_tstamp <= '{end}' "
            f"ORDER BY original_tstamp DESC LIMIT 1000"
        )

        conn = _get_connection()
        try:
            result = _execute(conn, sql)
            return {"events": result["rows"], "event_name": event_name, "date_range": date_range}
        finally:
            conn.close()

    def query_cohort(
        self,
        cohort_property: str,
        metric: str,
        date_range: str = "last_90d",
    ) -> dict:
        start, end = _parse_date_range(date_range)
        table_ref = _resolve_table(self.catalog, [metric])
        date_col = _get_date_column(table_ref)
        sql = (
            f"SELECT DATE_TRUNC('month', {cohort_property}) as cohort, "
            f"SUM({metric}) as {metric} "
            f"FROM {table_ref} f "
            f"WHERE {date_col} >= '{start}' AND {date_col} <= '{end}' "
            f"GROUP BY 1 ORDER BY 1"
        )

        conn = _get_connection()
        try:
            result = _execute(conn, sql)
            return {"data": result["rows"], "cohort_property": cohort_property, "date_range": date_range}
        finally:
            conn.close()

    def query_sql(self, sql: str) -> dict:
        conn = _get_connection()
        try:
            return _execute(conn, sql)
        finally:
            conn.close()

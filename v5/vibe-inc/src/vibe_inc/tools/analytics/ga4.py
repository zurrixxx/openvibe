"""GA4 analytics provider — wraps BetaAnalyticsDataClient into AnalyticsProvider.

Refactored from tools/ga4.py. The old ga4_read function is kept as a thin
backward-compat wrapper during migration.
"""
import os


def _get_client():
    """Initialize GA4 Data API client."""
    from google.analytics.data_v1beta import BetaAnalyticsDataClient

    sa_path = os.environ.get("GA4_SERVICE_ACCOUNT_JSON")
    if sa_path:
        return BetaAnalyticsDataClient.from_service_account_json(sa_path)
    return BetaAnalyticsDataClient()


def _parse_date_range(date_range: str):
    """Convert date_range to GA4 DateRange params."""
    from google.analytics.data_v1beta.types import DateRange

    if "," in date_range:
        start, end = date_range.split(",", 1)
        return DateRange(start_date=start.strip(), end_date=end.strip())
    days = {"last_7d": "7daysAgo", "last_28d": "28daysAgo", "last_90d": "90daysAgo", "last_24h": "1daysAgo"}
    return DateRange(start_date=days.get(date_range, "7daysAgo"), end_date="today")


def _run_report(client, property_id, metrics, dimensions=None, date_range="last_7d", dimension_filter=None):
    """Shared report runner for GA4."""
    from google.analytics.data_v1beta.types import (
        Dimension, Filter, FilterExpression,
        FilterExpressionList, Metric, RunReportRequest,
    )

    dr = _parse_date_range(date_range)
    request = RunReportRequest(
        property=f"properties/{property_id}",
        metrics=[Metric(name=m) for m in metrics],
        dimensions=[Dimension(name=d) for d in (dimensions or [])],
        date_ranges=[dr],
    )

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

    return rows


class GA4Provider:
    """GA4 analytics provider implementing the AnalyticsProvider protocol."""

    def __init__(self, property_id: str | None = None):
        self.property_id = property_id or os.environ.get("GA4_PROPERTY_ID", "")

    def query_metrics(
        self,
        metrics: list[str],
        dimensions: list[str] | None = None,
        date_range: str = "last_7d",
        filters: dict | None = None,
    ) -> dict:
        client = _get_client()
        rows = _run_report(client, self.property_id, metrics, dimensions, date_range, filters)
        return {"results": rows, "date_range": date_range}

    def query_funnel(
        self,
        steps: list[str],
        date_range: str = "last_7d",
        filters: dict | None = None,
    ) -> dict:
        client = _get_client()
        rows = _run_report(
            client, self.property_id,
            metrics=["eventCount"],
            dimensions=["eventName"],
            date_range=date_range,
            dimension_filter={"eventName": steps},
        )
        return {"data": rows, "steps": steps, "date_range": date_range}

    def query_events(
        self,
        event_name: str,
        date_range: str = "last_7d",
        properties: list[str] | None = None,
        filters: dict | None = None,
    ) -> dict:
        client = _get_client()
        dimensions = ["eventName"] + (properties or [])
        rows = _run_report(
            client, self.property_id,
            metrics=["eventCount"],
            dimensions=dimensions,
            date_range=date_range,
            dimension_filter={"eventName": [event_name]},
        )
        return {"events": rows, "event_name": event_name, "date_range": date_range}

    def query_cohort(
        self,
        cohort_property: str,
        metric: str,
        date_range: str = "last_90d",
    ) -> dict:
        client = _get_client()
        rows = _run_report(
            client, self.property_id,
            metrics=[metric],
            dimensions=[cohort_property],
            date_range=date_range,
        )
        return {"data": rows, "cohort_property": cohort_property, "date_range": date_range}

    def query_sql(self, sql: str) -> dict:
        raise NotImplementedError("GA4 does not support raw SQL. Use RedshiftProvider.")

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

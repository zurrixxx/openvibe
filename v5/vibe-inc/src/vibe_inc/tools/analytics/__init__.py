"""Analytics abstraction layer — unified query interface for Mixpanel, GA4, Redshift."""
from typing import Protocol, runtime_checkable


@runtime_checkable
class AnalyticsProvider(Protocol):
    """Unified analytics interface. Each data source implements this."""

    def query_metrics(
        self,
        metrics: list[str],
        dimensions: list[str] | None = None,
        date_range: str = "last_7d",
        filters: dict | None = None,
    ) -> dict:
        """Aggregated metrics. e.g. sessions, conversions, revenue by channel."""
        ...

    def query_funnel(
        self,
        steps: list[str],
        date_range: str = "last_7d",
        filters: dict | None = None,
    ) -> dict:
        """Funnel drop-off analysis."""
        ...

    def query_events(
        self,
        event_name: str,
        date_range: str = "last_7d",
        properties: list[str] | None = None,
        filters: dict | None = None,
    ) -> dict:
        """Raw event stream with property breakdowns."""
        ...

    def query_cohort(
        self,
        cohort_property: str,
        metric: str,
        date_range: str = "last_90d",
    ) -> dict:
        """Cohort analysis. e.g. retention by signup week."""
        ...

    def query_sql(self, sql: str) -> dict:
        """Raw SQL. Redshift only. Errors on other providers."""
        ...

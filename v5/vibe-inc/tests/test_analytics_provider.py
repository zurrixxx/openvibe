from typing import Protocol


def test_analytics_provider_protocol_exists():
    from vibe_inc.tools.analytics import AnalyticsProvider
    assert hasattr(AnalyticsProvider, "query_metrics")
    assert hasattr(AnalyticsProvider, "query_funnel")
    assert hasattr(AnalyticsProvider, "query_events")
    assert hasattr(AnalyticsProvider, "query_cohort")
    assert hasattr(AnalyticsProvider, "query_sql")


def test_analytics_provider_is_protocol():
    from vibe_inc.tools.analytics import AnalyticsProvider
    assert issubclass(AnalyticsProvider, Protocol)

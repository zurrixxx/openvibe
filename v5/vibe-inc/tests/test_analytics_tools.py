from unittest.mock import patch, MagicMock


def test_analytics_query_metrics_has_docstring():
    from vibe_inc.tools.analytics_tools import analytics_query_metrics
    assert analytics_query_metrics.__doc__ is not None


def test_default_provider_is_redshift():
    from vibe_inc.tools.analytics_tools import _get_provider
    from vibe_inc.tools.analytics.redshift import RedshiftProvider
    provider = _get_provider()
    assert isinstance(provider, RedshiftProvider)


def test_analytics_query_metrics_returns_dict():
    from vibe_inc.tools.analytics_tools import analytics_query_metrics

    mock_provider = MagicMock()
    mock_provider.query_metrics.return_value = {"rows": [], "date_range": "last_7d"}

    with patch("vibe_inc.tools.analytics_tools._get_provider", return_value=mock_provider):
        result = analytics_query_metrics(metrics=["spend_in_usd"], date_range="last_7d")

    assert isinstance(result, dict)


def test_analytics_query_funnel_returns_dict():
    from vibe_inc.tools.analytics_tools import analytics_query_funnel

    mock_provider = MagicMock()
    mock_provider.query_funnel.return_value = {"data": []}

    with patch("vibe_inc.tools.analytics_tools._get_provider", return_value=mock_provider):
        result = analytics_query_funnel(
            steps=["visitor_add_to_cart", "visitor_init_checkout", "visitor_close_won"],
        )

    assert isinstance(result, dict)


def test_analytics_query_sql_returns_dict():
    from vibe_inc.tools.analytics_tools import analytics_query_sql

    mock_provider = MagicMock()
    mock_provider.query_sql.return_value = {"rows": []}

    with patch("vibe_inc.tools.analytics_tools._get_provider", return_value=mock_provider):
        result = analytics_query_sql(sql="SELECT 1")

    assert isinstance(result, dict)


def test_analytics_query_events_returns_dict():
    from vibe_inc.tools.analytics_tools import analytics_query_events

    mock_provider = MagicMock()
    mock_provider.query_events.return_value = {"events": []}

    with patch("vibe_inc.tools.analytics_tools._get_provider", return_value=mock_provider):
        result = analytics_query_events(event_name="visitor_close_won")

    assert isinstance(result, dict)


def test_analytics_query_cohort_returns_dict():
    from vibe_inc.tools.analytics_tools import analytics_query_cohort

    mock_provider = MagicMock()
    mock_provider.query_cohort.return_value = {"data": []}

    with patch("vibe_inc.tools.analytics_tools._get_provider", return_value=mock_provider):
        result = analytics_query_cohort(cohort_property="created_at", metric="net_sales")

    assert isinstance(result, dict)

from unittest.mock import patch, MagicMock


def _mock_ga4_response(rows=None):
    mock_response = MagicMock()
    if rows is None:
        mock_row = MagicMock()
        mock_row.dimension_values = [MagicMock(value="organic")]
        mock_row.metric_values = [MagicMock(value="1000")]
        mock_response.rows = [mock_row]
    else:
        mock_response.rows = rows
    return mock_response


def test_ga4_provider_implements_protocol():
    from vibe_inc.tools.analytics import AnalyticsProvider
    from vibe_inc.tools.analytics.ga4 import GA4Provider

    provider = GA4Provider(property_id="12345")
    assert isinstance(provider, AnalyticsProvider)


def test_query_metrics_calls_run_report():
    from vibe_inc.tools.analytics.ga4 import GA4Provider

    mock_client = MagicMock()
    mock_client.run_report.return_value = _mock_ga4_response()

    with patch("vibe_inc.tools.analytics.ga4._get_client", return_value=mock_client):
        provider = GA4Provider(property_id="12345")
        result = provider.query_metrics(
            metrics=["sessions"],
            dimensions=["sessionDefaultChannelGroup"],
            date_range="last_7d",
        )

    assert "results" in result
    mock_client.run_report.assert_called_once()


def test_query_funnel_calls_run_report():
    from vibe_inc.tools.analytics.ga4 import GA4Provider

    mock_client = MagicMock()
    mock_client.run_report.return_value = _mock_ga4_response(rows=[])

    with patch("vibe_inc.tools.analytics.ga4._get_client", return_value=mock_client):
        provider = GA4Provider(property_id="12345")
        result = provider.query_funnel(
            steps=["page_view", "add_to_cart", "purchase"],
            date_range="last_7d",
        )

    assert "data" in result
    mock_client.run_report.assert_called_once()


def test_query_sql_raises_not_supported():
    from vibe_inc.tools.analytics.ga4 import GA4Provider
    import pytest

    provider = GA4Provider(property_id="12345")
    with pytest.raises(NotImplementedError):
        provider.query_sql("SELECT 1")

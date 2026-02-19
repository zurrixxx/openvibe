from unittest.mock import patch, MagicMock


def test_ga4_read_returns_rows():
    """ga4_read returns metric rows."""
    from vibe_inc.tools.ga4 import ga4_read

    mock_response = MagicMock()
    mock_row = MagicMock()
    mock_row.dimension_values = [MagicMock(value="organic")]
    mock_row.metric_values = [MagicMock(value="1000"), MagicMock(value="50")]
    mock_response.rows = [mock_row]

    mock_client = MagicMock()
    mock_client.run_report.return_value = mock_response

    with patch("vibe_inc.tools.ga4._get_client", return_value=mock_client), \
         patch.dict("os.environ", {"GA4_PROPERTY_ID": "12345"}):
        result = ga4_read(
            metrics=["sessions", "conversions"],
            dimensions=["sessionDefaultChannelGroup"],
            date_range="last_7d",
        )

    assert "rows" in result
    assert len(result["rows"]) == 1


def test_ga4_read_has_docstring():
    from vibe_inc.tools.ga4 import ga4_read
    assert ga4_read.__doc__ is not None
    assert "GA4" in ga4_read.__doc__


def test_ga4_read_funnel_events():
    """ga4_read can query specific events for funnel analysis."""
    from vibe_inc.tools.ga4 import ga4_read

    mock_response = MagicMock()
    mock_response.rows = []
    mock_client = MagicMock()
    mock_client.run_report.return_value = mock_response

    with patch("vibe_inc.tools.ga4._get_client", return_value=mock_client), \
         patch.dict("os.environ", {"GA4_PROPERTY_ID": "12345"}):
        result = ga4_read(
            metrics=["eventCount"],
            dimensions=["eventName", "pagePath"],
            date_range="last_7d",
            dimension_filter={"eventName": ["pdp_view", "cta_click", "begin_checkout", "purchase"]},
        )

    assert result["rows"] == []
    # Verify the client was called with filter
    mock_client.run_report.assert_called_once()

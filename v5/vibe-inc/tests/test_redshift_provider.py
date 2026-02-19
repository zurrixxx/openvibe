from unittest.mock import patch, MagicMock


def test_redshift_provider_implements_protocol():
    from vibe_inc.tools.analytics import AnalyticsProvider
    from vibe_inc.tools.analytics.redshift import RedshiftProvider
    provider = RedshiftProvider()
    assert isinstance(provider, AnalyticsProvider)


def test_redshift_loads_catalog():
    from vibe_inc.tools.analytics.redshift import RedshiftProvider
    provider = RedshiftProvider()
    assert provider.catalog is not None
    tables = {t["name"] for t in provider.catalog["tables"]}
    assert "fct_ads_ad_metrics" in tables
    assert "fct_order" in tables


def test_query_metrics_generates_sql():
    from vibe_inc.tools.analytics.redshift import RedshiftProvider

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        ("facebook", 1500.0, 50000, 1200),
        ("google", 2300.0, 80000, 2100),
    ]
    mock_cursor.description = [
        ("platform",), ("spend_in_usd",), ("impressions",), ("clicks",),
    ]

    with patch("vibe_inc.tools.analytics.redshift._get_connection", return_value=mock_conn):
        provider = RedshiftProvider()
        result = provider.query_metrics(
            metrics=["spend_in_usd", "impressions", "clicks"],
            dimensions=["platform"],
            date_range="last_7d",
        )

    assert "rows" in result
    assert len(result["rows"]) == 2
    assert result["rows"][0]["platform"] == "facebook"
    # Verify SQL was executed
    mock_cursor.execute.assert_called_once()
    sql = mock_cursor.execute.call_args[0][0]
    assert "fct_ads_ad_metrics" in sql
    assert "spend_in_usd" in sql


def test_query_metrics_joins_dimension():
    from vibe_inc.tools.analytics.redshift import RedshiftProvider

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [("Brand Campaign", 500.0)]
    mock_cursor.description = [("campaign_name",), ("spend_in_usd",)]

    with patch("vibe_inc.tools.analytics.redshift._get_connection", return_value=mock_conn):
        provider = RedshiftProvider()
        result = provider.query_metrics(
            metrics=["spend_in_usd"],
            dimensions=["campaign_name"],
            date_range="last_7d",
        )

    sql = mock_cursor.execute.call_args[0][0]
    assert "dim_ads_campaign" in sql
    assert "JOIN" in sql.upper()


def test_query_funnel_generates_conversion_sql():
    from vibe_inc.tools.analytics.redshift import RedshiftProvider

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        ("visitor_add_to_cart", 500),
        ("visitor_init_checkout", 200),
        ("visitor_close_won", 50),
    ]
    mock_cursor.description = [("conversion",), ("count",)]

    with patch("vibe_inc.tools.analytics.redshift._get_connection", return_value=mock_conn):
        provider = RedshiftProvider()
        result = provider.query_funnel(
            steps=["visitor_add_to_cart", "visitor_init_checkout", "visitor_close_won"],
            date_range="last_7d",
        )

    assert "data" in result
    sql = mock_cursor.execute.call_args[0][0]
    assert "fct_website_visitor_conversion" in sql


def test_query_sql_executes_raw():
    from vibe_inc.tools.analytics.redshift import RedshiftProvider

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [(42,)]
    mock_cursor.description = [("result",)]

    with patch("vibe_inc.tools.analytics.redshift._get_connection", return_value=mock_conn):
        provider = RedshiftProvider()
        result = provider.query_sql("SELECT 42 as result")

    assert result["rows"] == [{"result": 42}]
    mock_cursor.execute.assert_called_once_with("SELECT 42 as result")


def test_query_events_generates_sql():
    from vibe_inc.tools.analytics.redshift import RedshiftProvider

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []
    mock_cursor.description = []

    with patch("vibe_inc.tools.analytics.redshift._get_connection", return_value=mock_conn):
        provider = RedshiftProvider()
        result = provider.query_events(
            event_name="visitor_close_won",
            date_range="last_7d",
        )

    assert "events" in result
    sql = mock_cursor.execute.call_args[0][0]
    assert "fct_website_visitor_conversion" in sql
    assert "visitor_close_won" in sql


def test_query_cohort_generates_sql():
    from vibe_inc.tools.analytics.redshift import RedshiftProvider

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [("2026-01", 100)]
    mock_cursor.description = [("cohort",), ("count",)]

    with patch("vibe_inc.tools.analytics.redshift._get_connection", return_value=mock_conn):
        provider = RedshiftProvider()
        result = provider.query_cohort(
            cohort_property="created_at",
            metric="net_sales",
            date_range="last_90d",
        )

    assert "data" in result

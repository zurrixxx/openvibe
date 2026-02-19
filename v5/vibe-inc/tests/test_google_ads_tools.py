from unittest.mock import patch, MagicMock


def test_google_ads_query_returns_rows():
    """google_ads_query executes GAQL and returns structured rows."""
    from vibe_inc.tools.ads.google_ads import google_ads_query

    mock_service = MagicMock()
    mock_service.search.return_value = [
        {"campaign.name": "Bot - Foundation", "metrics.clicks": "200"},
    ]
    mock_client = MagicMock()
    mock_client.get_service.return_value = mock_service

    with patch("vibe_inc.tools.ads.google_ads._get_client", return_value=mock_client), \
         patch("vibe_inc.tools.ads.google_ads._get_customer_id", return_value="123-456-7890"):
        result = google_ads_query(query="SELECT campaign.name FROM campaign")

    assert "rows" in result
    assert len(result["rows"]) == 1
    assert result["query"] == "SELECT campaign.name FROM campaign"


def test_google_ads_query_has_docstring():
    """Tool function must have a docstring for Anthropic schema generation."""
    from vibe_inc.tools.ads.google_ads import google_ads_query
    assert google_ads_query.__doc__ is not None
    assert "GAQL" in google_ads_query.__doc__


def test_google_ads_mutate_returns_results():
    """google_ads_mutate applies operations and returns resource names."""
    from vibe_inc.tools.ads.google_ads import google_ads_mutate

    mock_result = MagicMock()
    mock_result.resource_name = "customers/123/campaigns/456"
    mock_response = MagicMock()
    mock_response.mutate_operation_responses = [mock_result]

    mock_service = MagicMock()
    mock_service.mutate.return_value = mock_response
    mock_client = MagicMock()
    mock_client.get_service.return_value = mock_service

    operations = [{"campaign_operation": {"create": {"name": "Test Campaign"}}}]

    with patch("vibe_inc.tools.ads.google_ads._get_client", return_value=mock_client), \
         patch("vibe_inc.tools.ads.google_ads._get_customer_id", return_value="123-456-7890"):
        result = google_ads_mutate(operations=operations)

    assert "results" in result
    assert result["results"] == ["customers/123/campaigns/456"]
    assert result["operation_count"] == 1


def test_google_ads_mutate_has_docstring():
    """Tool function must have a docstring for Anthropic schema generation."""
    from vibe_inc.tools.ads.google_ads import google_ads_mutate
    assert google_ads_mutate.__doc__ is not None
    assert "mutation" in google_ads_mutate.__doc__.lower()


def test_google_ads_budget_reads_current():
    """google_ads_budget reads current budget and returns USD conversion."""
    from vibe_inc.tools.ads.google_ads import google_ads_budget

    mock_row = MagicMock()
    mock_row.campaign_budget.amount_micros = 50_000_000  # $50

    mock_service = MagicMock()
    mock_service.search.return_value = [mock_row]
    mock_client = MagicMock()
    mock_client.get_service.return_value = mock_service

    with patch("vibe_inc.tools.ads.google_ads._get_client", return_value=mock_client), \
         patch("vibe_inc.tools.ads.google_ads._get_customer_id", return_value="123-456-7890"):
        result = google_ads_budget(campaign_id="789")

    assert result["campaign_id"] == "789"
    assert result["budget_micros"] == 50_000_000
    assert result["budget_usd"] == 50.0


def test_google_ads_recommendations_returns_list():
    """google_ads_recommendations returns optimization recommendations."""
    from vibe_inc.tools.ads.google_ads import google_ads_recommendations

    mock_service = MagicMock()
    mock_service.search.return_value = [
        {"recommendation.type": "KEYWORD", "recommendation.impact": "HIGH"},
        {"recommendation.type": "TEXT_AD", "recommendation.impact": "MEDIUM"},
    ]
    mock_client = MagicMock()
    mock_client.get_service.return_value = mock_service

    with patch("vibe_inc.tools.ads.google_ads._get_client", return_value=mock_client), \
         patch("vibe_inc.tools.ads.google_ads._get_customer_id", return_value="123-456-7890"):
        result = google_ads_recommendations()

    assert "recommendations" in result
    assert len(result["recommendations"]) == 2


def test_google_ads_conversions_returns_rows():
    """google_ads_conversions returns conversion data with date range."""
    from vibe_inc.tools.ads.google_ads import google_ads_conversions

    mock_service = MagicMock()
    mock_service.search.return_value = [
        {"campaign.name": "Bot - Foundation", "metrics.conversions": "15",
         "metrics.cost_micros": "75000000"},
    ]
    mock_client = MagicMock()
    mock_client.get_service.return_value = mock_service

    with patch("vibe_inc.tools.ads.google_ads._get_client", return_value=mock_client), \
         patch("vibe_inc.tools.ads.google_ads._get_customer_id", return_value="123-456-7890"):
        result = google_ads_conversions(date_range="LAST_30_DAYS")

    assert "rows" in result
    assert len(result["rows"]) == 1
    assert result["date_range"] == "LAST_30_DAYS"

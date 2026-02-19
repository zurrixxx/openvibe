from unittest.mock import patch, MagicMock


def _mock_response(json_data=None, headers=None):
    """Create a mock httpx response."""
    resp = MagicMock()
    resp.json.return_value = json_data or {}
    resp.raise_for_status.return_value = None
    resp.headers = headers or {}
    return resp


def test_linkedin_ads_analytics_returns_rows():
    """linkedin_ads_analytics returns structured analytics data with rows."""
    from vibe_inc.tools.ads.linkedin_ads import linkedin_ads_analytics

    mock_resp = _mock_response(json_data={
        "elements": [
            {"impressions": 5000, "clicks": 120, "costInLocalCurrency": "350.00"},
        ],
    })

    with patch("vibe_inc.tools.ads.linkedin_ads.httpx") as mock_httpx, \
         patch("vibe_inc.tools.ads.linkedin_ads._get_headers", return_value={"Authorization": "Bearer test"}), \
         patch("vibe_inc.tools.ads.linkedin_ads._get_account_id", return_value="12345"):
        mock_httpx.get.return_value = mock_resp
        result = linkedin_ads_analytics(date_range="last_7d", granularity="DAILY")

    assert "rows" in result
    assert len(result["rows"]) == 1
    assert result["date_range"] == "last_7d"
    assert result["granularity"] == "DAILY"


def test_linkedin_ads_analytics_has_docstring():
    """Tool function must have a docstring for Anthropic schema generation."""
    from vibe_inc.tools.ads.linkedin_ads import linkedin_ads_analytics
    assert linkedin_ads_analytics.__doc__ is not None
    assert "analytics" in linkedin_ads_analytics.__doc__.lower()


def test_linkedin_ads_campaigns_returns_list():
    """linkedin_ads_campaigns returns a list of campaigns."""
    from vibe_inc.tools.ads.linkedin_ads import linkedin_ads_campaigns

    mock_resp = _mock_response(json_data={
        "elements": [
            {"id": "camp_1", "name": "Vibe Bot - B2B", "status": "ACTIVE"},
            {"id": "camp_2", "name": "Vibe Dot - IT Leaders", "status": "PAUSED"},
        ],
    })

    with patch("vibe_inc.tools.ads.linkedin_ads.httpx") as mock_httpx, \
         patch("vibe_inc.tools.ads.linkedin_ads._get_headers", return_value={"Authorization": "Bearer test"}), \
         patch("vibe_inc.tools.ads.linkedin_ads._get_account_id", return_value="12345"):
        mock_httpx.get.return_value = mock_resp
        result = linkedin_ads_campaigns()

    assert "campaigns" in result
    assert len(result["campaigns"]) == 2


def test_linkedin_ads_create_returns_id():
    """linkedin_ads_create returns a campaign_id for the new campaign."""
    from vibe_inc.tools.ads.linkedin_ads import linkedin_ads_create

    mock_resp = _mock_response(
        json_data={"id": "new_camp_789"},
        headers={"x-restli-id": "new_camp_789"},
    )

    with patch("vibe_inc.tools.ads.linkedin_ads.httpx") as mock_httpx, \
         patch("vibe_inc.tools.ads.linkedin_ads._get_headers", return_value={"Authorization": "Bearer test"}), \
         patch("vibe_inc.tools.ads.linkedin_ads._get_account_id", return_value="12345"):
        mock_httpx.post.return_value = mock_resp
        result = linkedin_ads_create(
            campaign_name="Vibe Bot - Decision Makers",
            objective="LEAD_GENERATION",
            audience={"job_titles": ["CTO", "VP Engineering"]},
            budget_daily=100.0,
        )

    assert "campaign_id" in result
    assert result["campaign_id"] == "new_camp_789"


def test_linkedin_ads_update_returns_result():
    """linkedin_ads_update returns updated=True on success."""
    from vibe_inc.tools.ads.linkedin_ads import linkedin_ads_update

    mock_resp = _mock_response()

    with patch("vibe_inc.tools.ads.linkedin_ads.httpx") as mock_httpx, \
         patch("vibe_inc.tools.ads.linkedin_ads._get_headers", return_value={"Authorization": "Bearer test"}):
        mock_httpx.post.return_value = mock_resp
        result = linkedin_ads_update(
            campaign_id="camp_123",
            updates={"status": "ACTIVE"},
        )

    assert result["updated"] is True
    assert result["campaign_id"] == "camp_123"


def test_linkedin_ads_audiences_returns_list():
    """linkedin_ads_audiences returns audience segments."""
    from vibe_inc.tools.ads.linkedin_ads import linkedin_ads_audiences

    mock_resp = _mock_response(json_data={
        "elements": [
            {"id": "seg_1", "name": "Website Visitors", "matchedCount": 15000},
            {"id": "seg_2", "name": "CTO Lookalike", "matchedCount": 250000},
        ],
    })

    with patch("vibe_inc.tools.ads.linkedin_ads.httpx") as mock_httpx, \
         patch("vibe_inc.tools.ads.linkedin_ads._get_headers", return_value={"Authorization": "Bearer test"}), \
         patch("vibe_inc.tools.ads.linkedin_ads._get_account_id", return_value="12345"):
        mock_httpx.get.return_value = mock_resp
        result = linkedin_ads_audiences()

    assert "audiences" in result
    assert len(result["audiences"]) == 2


def test_linkedin_ads_conversions_returns_data():
    """linkedin_ads_conversions returns conversion tracking data."""
    from vibe_inc.tools.ads.linkedin_ads import linkedin_ads_conversions

    mock_resp = _mock_response(json_data={
        "elements": [
            {"conversionId": "conv_1", "conversionValueInLocalCurrency": "500.00"},
        ],
    })

    with patch("vibe_inc.tools.ads.linkedin_ads.httpx") as mock_httpx, \
         patch("vibe_inc.tools.ads.linkedin_ads._get_headers", return_value={"Authorization": "Bearer test"}), \
         patch("vibe_inc.tools.ads.linkedin_ads._get_account_id", return_value="12345"):
        mock_httpx.get.return_value = mock_resp
        result = linkedin_ads_conversions(date_range="last_7d")

    assert "conversions" in result
    assert len(result["conversions"]) == 1
    assert result["date_range"] == "last_7d"

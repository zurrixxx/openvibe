from unittest.mock import patch, MagicMock


def test_amazon_ads_report_three_step_flow():
    """amazon_ads_report executes 3-step async flow: request -> poll -> download."""
    from vibe_inc.tools.ads.amazon_ads import amazon_ads_report

    mock_rows = [
        {"impressions": "5000", "clicks": "120", "spend": "45.00"},
        {"impressions": "3200", "clicks": "80", "spend": "30.50"},
    ]

    with patch("vibe_inc.tools.ads.amazon_ads._get_client", return_value={"client_id": "x", "client_secret": "s", "refresh_token": "t", "profile_id": "p"}), \
         patch("vibe_inc.tools.ads.amazon_ads._request_report", return_value="report-123"), \
         patch("vibe_inc.tools.ads.amazon_ads._poll_report", return_value="https://download.example.com/report.gz"), \
         patch("vibe_inc.tools.ads.amazon_ads._download_report", return_value=mock_rows):
        result = amazon_ads_report(
            ad_product="SPONSORED_PRODUCTS",
            report_type="spCampaigns",
            columns=["impressions", "clicks", "spend"],
            date_range="last_7d",
        )

    assert "rows" in result
    assert len(result["rows"]) == 2
    assert result["ad_product"] == "SPONSORED_PRODUCTS"
    assert result["report_type"] == "spCampaigns"


def test_amazon_ads_report_has_docstring():
    """Tool function must have a docstring for Anthropic schema generation."""
    from vibe_inc.tools.ads.amazon_ads import amazon_ads_report
    assert amazon_ads_report.__doc__ is not None
    assert "report" in amazon_ads_report.__doc__.lower()


def test_amazon_ads_campaigns_returns_list():
    """amazon_ads_campaigns returns a list of campaigns."""
    from vibe_inc.tools.ads.amazon_ads import amazon_ads_campaigns

    mock_resp = MagicMock()
    mock_resp.json.return_value = [
        {"campaignId": "camp_1", "name": "SP - Brand", "state": "enabled"},
        {"campaignId": "camp_2", "name": "SP - Category", "state": "paused"},
    ]
    mock_resp.raise_for_status = MagicMock()

    with patch("vibe_inc.tools.ads.amazon_ads._get_client", return_value={"client_id": "x", "client_secret": "s", "refresh_token": "t", "profile_id": "p"}), \
         patch("vibe_inc.tools.ads.amazon_ads.httpx") as mock_httpx:
        mock_httpx.get.return_value = mock_resp
        result = amazon_ads_campaigns(ad_product="SPONSORED_PRODUCTS")

    assert "campaigns" in result
    assert len(result["campaigns"]) == 2
    assert result["ad_product"] == "SPONSORED_PRODUCTS"


def test_amazon_ads_campaigns_has_docstring():
    """Tool function must have a docstring."""
    from vibe_inc.tools.ads.amazon_ads import amazon_ads_campaigns
    assert amazon_ads_campaigns.__doc__ is not None
    assert "campaign" in amazon_ads_campaigns.__doc__.lower()


def test_amazon_ads_keywords_returns_list():
    """amazon_ads_keywords returns keywords for a campaign."""
    from vibe_inc.tools.ads.amazon_ads import amazon_ads_keywords

    mock_resp = MagicMock()
    mock_resp.json.return_value = [
        {"keywordId": "kw_1", "keywordText": "wireless speaker", "bid": 1.50},
        {"keywordId": "kw_2", "keywordText": "bluetooth speaker", "bid": 2.00},
    ]
    mock_resp.raise_for_status = MagicMock()

    with patch("vibe_inc.tools.ads.amazon_ads._get_client", return_value={"client_id": "x", "client_secret": "s", "refresh_token": "t", "profile_id": "p"}), \
         patch("vibe_inc.tools.ads.amazon_ads.httpx") as mock_httpx:
        mock_httpx.get.return_value = mock_resp
        result = amazon_ads_keywords(campaign_id="camp_1")

    assert "keywords" in result
    assert len(result["keywords"]) == 2
    assert result["campaign_id"] == "camp_1"


def test_amazon_ads_bid_update_returns_result():
    """amazon_ads_bid_update returns updated=True on success."""
    from vibe_inc.tools.ads.amazon_ads import amazon_ads_bid_update

    mock_resp = MagicMock()
    mock_resp.json.return_value = [{"keywordId": "98765", "code": "SUCCESS"}]
    mock_resp.raise_for_status = MagicMock()

    with patch("vibe_inc.tools.ads.amazon_ads._get_client", return_value={"client_id": "x", "client_secret": "s", "refresh_token": "t", "profile_id": "p"}), \
         patch("vibe_inc.tools.ads.amazon_ads.httpx") as mock_httpx:
        mock_httpx.put.return_value = mock_resp
        result = amazon_ads_bid_update(
            campaign_id="12345",
            ad_group_id="67890",
            keyword_id="98765",
            new_bid=2.50,
        )

    assert result["updated"] is True
    assert result["keyword_id"] == "98765"
    assert result["new_bid"] == 2.50


def test_amazon_ads_budget_reads_current():
    """amazon_ads_budget reads current budget when new_budget is None."""
    from vibe_inc.tools.ads.amazon_ads import amazon_ads_budget

    mock_resp = MagicMock()
    mock_resp.json.return_value = {"campaignId": "camp_1", "dailyBudget": 100.0, "name": "SP - Brand"}
    mock_resp.raise_for_status = MagicMock()

    with patch("vibe_inc.tools.ads.amazon_ads._get_client", return_value={"client_id": "x", "client_secret": "s", "refresh_token": "t", "profile_id": "p"}), \
         patch("vibe_inc.tools.ads.amazon_ads.httpx") as mock_httpx:
        mock_httpx.get.return_value = mock_resp
        result = amazon_ads_budget(campaign_id="camp_1")

    assert result["campaign_id"] == "camp_1"
    assert result["budget"] == 100.0
    assert result["updated"] is False


def test_amazon_ads_search_terms_returns_list():
    """amazon_ads_search_terms returns filtered search terms for a campaign."""
    from vibe_inc.tools.ads.amazon_ads import amazon_ads_search_terms

    mock_rows = [
        {"searchTerm": "wireless speaker", "impressions": "500", "clicks": "20", "campaignId": "camp_1"},
        {"searchTerm": "bluetooth speaker", "impressions": "300", "clicks": "15", "campaignId": "camp_1"},
        {"searchTerm": "other term", "impressions": "100", "clicks": "5", "campaignId": "camp_2"},
    ]

    with patch("vibe_inc.tools.ads.amazon_ads._get_client", return_value={"client_id": "x", "client_secret": "s", "refresh_token": "t", "profile_id": "p"}), \
         patch("vibe_inc.tools.ads.amazon_ads._request_report", return_value="report-456"), \
         patch("vibe_inc.tools.ads.amazon_ads._poll_report", return_value="https://download.example.com/st.gz"), \
         patch("vibe_inc.tools.ads.amazon_ads._download_report", return_value=mock_rows):
        result = amazon_ads_search_terms(campaign_id="camp_1", date_range="last_7d")

    assert "search_terms" in result
    assert len(result["search_terms"]) == 2
    assert result["campaign_id"] == "camp_1"
    assert all(row["campaignId"] == "camp_1" for row in result["search_terms"])

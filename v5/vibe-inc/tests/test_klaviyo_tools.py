from unittest.mock import patch, MagicMock


def _mock_response(json_data):
    """Create a mock httpx response with .json() returning given data."""
    resp = MagicMock()
    resp.json.return_value = json_data
    return resp


def test_klaviyo_campaigns_returns_list():
    """klaviyo_campaigns returns campaign list from GET endpoint."""
    from vibe_inc.tools.commerce.klaviyo import klaviyo_campaigns

    mock_resp = _mock_response({
        "data": [
            {"id": "camp_1", "attributes": {"name": "Welcome Flow", "status": "sent"}},
            {"id": "camp_2", "attributes": {"name": "Flash Sale", "status": "draft"}},
        ],
    })

    with patch("vibe_inc.tools.commerce.klaviyo.httpx") as mock_httpx, \
         patch("vibe_inc.tools.commerce.klaviyo._get_headers", return_value={"Authorization": "Klaviyo-API-Key test"}):
        mock_httpx.get.return_value = mock_resp
        result = klaviyo_campaigns()

    assert "campaigns" in result
    assert len(result["campaigns"]) == 2


def test_klaviyo_campaigns_has_docstring():
    """Tool function must have a docstring for Anthropic schema generation."""
    from vibe_inc.tools.commerce.klaviyo import klaviyo_campaigns
    assert klaviyo_campaigns.__doc__ is not None
    assert "Klaviyo" in klaviyo_campaigns.__doc__


def test_klaviyo_flows_returns_list():
    """klaviyo_flows returns automation flows list."""
    from vibe_inc.tools.commerce.klaviyo import klaviyo_flows

    mock_resp = _mock_response({
        "data": [
            {"id": "flow_1", "attributes": {"name": "Welcome Series", "status": "live"}},
        ],
    })

    with patch("vibe_inc.tools.commerce.klaviyo.httpx") as mock_httpx, \
         patch("vibe_inc.tools.commerce.klaviyo._get_headers", return_value={"Authorization": "Klaviyo-API-Key test"}):
        mock_httpx.get.return_value = mock_resp
        result = klaviyo_flows()

    assert "flows" in result
    assert len(result["flows"]) == 1


def test_klaviyo_segments_returns_list():
    """klaviyo_segments returns segment list."""
    from vibe_inc.tools.commerce.klaviyo import klaviyo_segments

    mock_resp = _mock_response({
        "data": [
            {"id": "seg_1", "attributes": {"name": "VIP Customers"}},
            {"id": "seg_2", "attributes": {"name": "Engaged 30d"}},
        ],
    })

    with patch("vibe_inc.tools.commerce.klaviyo.httpx") as mock_httpx, \
         patch("vibe_inc.tools.commerce.klaviyo._get_headers", return_value={"Authorization": "Klaviyo-API-Key test"}):
        mock_httpx.get.return_value = mock_resp
        result = klaviyo_segments()

    assert "segments" in result
    assert len(result["segments"]) == 2


def test_klaviyo_metrics_returns_data():
    """klaviyo_metrics returns metric definitions or aggregate data."""
    from vibe_inc.tools.commerce.klaviyo import klaviyo_metrics

    mock_resp = _mock_response({
        "data": [
            {"id": "metric_1", "attributes": {"name": "Opened Email"}},
            {"id": "metric_2", "attributes": {"name": "Clicked Email"}},
        ],
    })

    with patch("vibe_inc.tools.commerce.klaviyo.httpx") as mock_httpx, \
         patch("vibe_inc.tools.commerce.klaviyo._get_headers", return_value={"Authorization": "Klaviyo-API-Key test"}):
        mock_httpx.get.return_value = mock_resp
        result = klaviyo_metrics()

    assert "metrics" in result
    assert len(result["metrics"]) == 2


def test_klaviyo_profiles_returns_list():
    """klaviyo_profiles returns profile list with count."""
    from vibe_inc.tools.commerce.klaviyo import klaviyo_profiles

    mock_resp = _mock_response({
        "data": [
            {"id": "prof_1", "attributes": {"email": "a@example.com"}},
            {"id": "prof_2", "attributes": {"email": "b@example.com"}},
        ],
    })

    with patch("vibe_inc.tools.commerce.klaviyo.httpx") as mock_httpx, \
         patch("vibe_inc.tools.commerce.klaviyo._get_headers", return_value={"Authorization": "Klaviyo-API-Key test"}):
        mock_httpx.get.return_value = mock_resp
        result = klaviyo_profiles()

    assert "profiles" in result
    assert "count" in result
    assert result["count"] == 2


def test_klaviyo_catalogs_returns_items():
    """klaviyo_catalogs returns catalog items list."""
    from vibe_inc.tools.commerce.klaviyo import klaviyo_catalogs

    mock_resp = _mock_response({
        "data": [
            {"id": "item_1", "attributes": {"title": "Vibe Bot", "price": 3299}},
        ],
    })

    with patch("vibe_inc.tools.commerce.klaviyo.httpx") as mock_httpx, \
         patch("vibe_inc.tools.commerce.klaviyo._get_headers", return_value={"Authorization": "Klaviyo-API-Key test"}):
        mock_httpx.get.return_value = mock_resp
        result = klaviyo_catalogs()

    assert "items" in result
    assert len(result["items"]) == 1

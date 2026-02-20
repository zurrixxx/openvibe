from unittest.mock import patch, MagicMock


def _mock_response(json_data):
    """Create a mock httpx response with .json() returning given data."""
    resp = MagicMock()
    resp.json.return_value = json_data
    return resp


def test_hubspot_contact_get_by_email():
    """hubspot_contact_get searches by email and returns contact with enrichment info."""
    from vibe_inc.tools.crm.hubspot import hubspot_contact_get

    mock_resp = _mock_response({
        "results": [
            {
                "id": "501",
                "properties": {
                    "email": "buyer@acme.com",
                    "firstname": "Jane",
                    "lastname": "Doe",
                    "company": "Acme Corp",
                    "lifecyclestage": "customer",
                    "hs_lead_status": "OPEN",
                },
            },
        ],
    })

    with patch("vibe_inc.tools.crm.hubspot.httpx") as mock_httpx, \
         patch("vibe_inc.tools.crm.hubspot._get_headers", return_value={"Authorization": "Bearer test"}):
        mock_httpx.post.return_value = mock_resp
        result = hubspot_contact_get(email="buyer@acme.com")

    assert "contact" in result
    assert result["contact"]["id"] == "501"
    assert result["contact"]["properties"]["company"] == "Acme Corp"


def test_hubspot_contact_get_has_docstring():
    """Tool function must have a docstring for Anthropic schema generation."""
    from vibe_inc.tools.crm.hubspot import hubspot_contact_get
    assert hubspot_contact_get.__doc__ is not None
    assert "HubSpot" in hubspot_contact_get.__doc__

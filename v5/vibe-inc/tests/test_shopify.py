from unittest.mock import patch, MagicMock


def test_shopify_page_read_returns_content():
    from vibe_inc.tools.shopify import shopify_page_read

    mock_page = {"id": 123, "title": "Vibebot", "body_html": "<h1>Bot</h1>"}
    with patch("vibe_inc.tools.shopify._get_page", return_value=mock_page):
        result = shopify_page_read(page_id="123")

    assert result["title"] == "Vibebot"
    assert "body_html" in result


def test_shopify_page_read_has_docstring():
    from vibe_inc.tools.shopify import shopify_page_read
    assert shopify_page_read.__doc__ is not None


def test_shopify_page_update_changes_content():
    from vibe_inc.tools.shopify import shopify_page_update

    mock_page = MagicMock()
    with patch("vibe_inc.tools.shopify._get_page_resource", return_value=mock_page):
        result = shopify_page_update(
            page_id="123",
            updates={"title": "New Title", "body_html": "<h1>Updated</h1>"},
        )

    assert result["updated"] is True
    assert result["page_id"] == "123"


def test_shopify_page_update_has_docstring():
    from vibe_inc.tools.shopify import shopify_page_update
    assert shopify_page_update.__doc__ is not None

from unittest.mock import patch, MagicMock


def _mock_response(json_data):
    resp = MagicMock()
    resp.json.return_value = json_data
    return resp


def test_shopify_products_returns_list():
    from vibe_inc.tools.commerce.shopify import shopify_products

    mock_resp = _mock_response({
        "products": [
            {"id": 1, "title": "Bot", "status": "active"},
            {"id": 2, "title": "Dot", "status": "active"},
        ],
    })

    with patch("vibe_inc.tools.commerce.shopify.httpx") as mock_httpx, \
         patch("vibe_inc.tools.commerce.shopify._get_headers", return_value={"X-Shopify-Access-Token": "test"}), \
         patch("vibe_inc.tools.commerce.shopify._get_base_url", return_value="https://test.myshopify.com/admin/api/2024-01"):
        mock_httpx.get.return_value = mock_resp
        result = shopify_products()

    assert "products" in result
    assert result["count"] == 2


def test_shopify_products_has_docstring():
    from vibe_inc.tools.commerce.shopify import shopify_products
    assert shopify_products.__doc__ is not None
    assert "Shopify" in shopify_products.__doc__


def test_shopify_orders_returns_list():
    from vibe_inc.tools.commerce.shopify import shopify_orders

    mock_resp = _mock_response({
        "orders": [
            {"id": 1, "total_price": "299.00"},
            {"id": 2, "total_price": "199.00"},
        ],
    })

    with patch("vibe_inc.tools.commerce.shopify.httpx") as mock_httpx, \
         patch("vibe_inc.tools.commerce.shopify._get_headers", return_value={"X-Shopify-Access-Token": "test"}), \
         patch("vibe_inc.tools.commerce.shopify._get_base_url", return_value="https://test.myshopify.com/admin/api/2024-01"):
        mock_httpx.get.return_value = mock_resp
        result = shopify_orders()

    assert "orders" in result
    assert result["count"] == 2
    assert result["total_revenue"] == 498.0


def test_shopify_orders_has_docstring():
    from vibe_inc.tools.commerce.shopify import shopify_orders
    assert shopify_orders.__doc__ is not None


def test_shopify_collections_returns_list():
    from vibe_inc.tools.commerce.shopify import shopify_collections

    mock_resp = _mock_response({
        "smart_collections": [
            {"id": 1, "title": "Hardware"},
        ],
    })

    with patch("vibe_inc.tools.commerce.shopify.httpx") as mock_httpx, \
         patch("vibe_inc.tools.commerce.shopify._get_headers", return_value={"X-Shopify-Access-Token": "test"}), \
         patch("vibe_inc.tools.commerce.shopify._get_base_url", return_value="https://test.myshopify.com/admin/api/2024-01"):
        mock_httpx.get.return_value = mock_resp
        result = shopify_collections(collection_type="smart")

    assert "collections" in result
    assert result["count"] == 1


def test_shopify_discounts_returns_list():
    from vibe_inc.tools.commerce.shopify import shopify_discounts

    mock_resp = _mock_response({
        "price_rules": [
            {"id": 1, "title": "LAUNCH10", "value": "-10.0"},
        ],
    })

    with patch("vibe_inc.tools.commerce.shopify.httpx") as mock_httpx, \
         patch("vibe_inc.tools.commerce.shopify._get_headers", return_value={"X-Shopify-Access-Token": "test"}), \
         patch("vibe_inc.tools.commerce.shopify._get_base_url", return_value="https://test.myshopify.com/admin/api/2024-01"):
        mock_httpx.get.return_value = mock_resp
        result = shopify_discounts()

    assert "discounts" in result
    assert result["count"] == 1


def test_shopify_collections_custom_type():
    from vibe_inc.tools.commerce.shopify import shopify_collections

    mock_resp = _mock_response({
        "custom_collections": [
            {"id": 1, "title": "Featured"},
        ],
    })

    with patch("vibe_inc.tools.commerce.shopify.httpx") as mock_httpx, \
         patch("vibe_inc.tools.commerce.shopify._get_headers", return_value={"X-Shopify-Access-Token": "test"}), \
         patch("vibe_inc.tools.commerce.shopify._get_base_url", return_value="https://test.myshopify.com/admin/api/2024-01"):
        mock_httpx.get.return_value = mock_resp
        result = shopify_collections(collection_type="custom")

    assert "collections" in result


def test_shopify_orders_calculates_revenue():
    from vibe_inc.tools.commerce.shopify import shopify_orders

    mock_resp = _mock_response({
        "orders": [
            {"id": 1, "total_price": "100.50"},
            {"id": 2, "total_price": "200.25"},
            {"id": 3, "total_price": "50.00"},
        ],
    })

    with patch("vibe_inc.tools.commerce.shopify.httpx") as mock_httpx, \
         patch("vibe_inc.tools.commerce.shopify._get_headers", return_value={"X-Shopify-Access-Token": "test"}), \
         patch("vibe_inc.tools.commerce.shopify._get_base_url", return_value="https://test.myshopify.com/admin/api/2024-01"):
        mock_httpx.get.return_value = mock_resp
        result = shopify_orders()

    assert result["total_revenue"] == 350.75

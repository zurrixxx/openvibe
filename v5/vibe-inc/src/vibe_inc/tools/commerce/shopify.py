"""Shopify Admin API tools — expanded for D2C Growth."""
import os

import httpx

_BASE_URL_TEMPLATE = "https://{store}.myshopify.com/admin/api/2024-01"


def _get_headers():
    """Return authorization headers for Shopify Admin API.

    Requires: SHOPIFY_ACCESS_TOKEN
    """
    return {"X-Shopify-Access-Token": os.environ["SHOPIFY_ACCESS_TOKEN"]}


def _get_base_url():
    """Return the base URL for the configured Shopify store."""
    store = os.environ["SHOPIFY_STORE"]
    return _BASE_URL_TEMPLATE.format(store=store)


def shopify_products(
    collection_id: str | None = None,
    status: str = "active",
    limit: int = 50,
) -> dict:
    """List Shopify products with optional collection filter.

    Args:
        collection_id: Optional collection ID to filter by.
        status: Product status filter (active, draft, archived).
        limit: Max products to return.

    Returns:
        Dict with products list and count.
    """
    url = f"{_get_base_url()}/products.json"
    params = {"status": status, "limit": limit}
    if collection_id:
        params["collection_id"] = collection_id
    resp = httpx.get(url, headers=_get_headers(), params=params)
    data = resp.json()
    products = data.get("products", [])
    return {"products": products, "count": len(products)}


def shopify_orders(
    status: str = "any",
    created_at_min: str | None = None,
    limit: int = 50,
) -> dict:
    """List Shopify orders with optional date and status filter.

    Args:
        status: Order status (any, open, closed, cancelled).
        created_at_min: ISO datetime for minimum creation date.
        limit: Max orders to return.

    Returns:
        Dict with orders list, count, and total revenue.
    """
    url = f"{_get_base_url()}/orders.json"
    params = {"status": status, "limit": limit}
    if created_at_min:
        params["created_at_min"] = created_at_min
    resp = httpx.get(url, headers=_get_headers(), params=params)
    data = resp.json()
    orders = data.get("orders", [])
    total_revenue = sum(float(o.get("total_price", 0)) for o in orders)
    return {"orders": orders, "count": len(orders), "total_revenue": total_revenue}


def shopify_collections(collection_type: str = "smart") -> dict:
    """List Shopify collections (smart or custom).

    Args:
        collection_type: Either 'smart' or 'custom'.

    Returns:
        Dict with collections list.
    """
    endpoint = "smart_collections" if collection_type == "smart" else "custom_collections"
    url = f"{_get_base_url()}/{endpoint}.json"
    resp = httpx.get(url, headers=_get_headers())
    data = resp.json()
    collections = data.get(endpoint, [])
    return {"collections": collections, "count": len(collections)}


def shopify_discounts(limit: int = 50) -> dict:
    """List Shopify price rules (discount codes).

    Args:
        limit: Max price rules to return.

    Returns:
        Dict with discounts list.
    """
    url = f"{_get_base_url()}/price_rules.json"
    resp = httpx.get(url, headers=_get_headers(), params={"limit": limit})
    data = resp.json()
    discounts = data.get("price_rules", [])
    return {"discounts": discounts, "count": len(discounts)}

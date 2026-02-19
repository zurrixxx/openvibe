"""Shopify Admin API tools for CROps operator."""
import os


def _get_session():
    """Create Shopify API session from environment.

    Requires: SHOPIFY_STORE, SHOPIFY_ACCESS_TOKEN
    """
    import shopify
    store = os.environ["SHOPIFY_STORE"]
    token = os.environ["SHOPIFY_ACCESS_TOKEN"]
    session = shopify.Session(f"{store}.myshopify.com", "2024-01", token)
    shopify.ShopifyResource.activate_session(session)
    return session


def _get_page(page_id: str) -> dict:
    """Fetch a page by ID."""
    import shopify
    _get_session()
    page = shopify.Page.find(page_id)
    return page.to_dict()


def _get_page_resource(page_id: str):
    """Fetch a page resource for updates."""
    import shopify
    _get_session()
    return shopify.Page.find(page_id)


def shopify_page_read(page_id: str) -> dict:
    """Read a Shopify page's content by ID.

    Args:
        page_id: The Shopify page ID.

    Returns:
        Dict with page fields: id, title, body_html, handle, published_at.
    """
    return _get_page(page_id)


def shopify_page_update(page_id: str, updates: dict) -> dict:
    """Update a Shopify page's content.

    Args:
        page_id: The Shopify page ID.
        updates: Fields to update (title, body_html, meta_title, meta_description).

    Returns:
        Dict with updated=True and the page_id.
    """
    page = _get_page_resource(page_id)
    for key, value in updates.items():
        setattr(page, key, value)
    page.save()
    return {"updated": True, "page_id": page_id, "fields_changed": list(updates.keys())}

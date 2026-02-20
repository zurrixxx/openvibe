"""Klaviyo email marketing tools for D2C Growth role."""
import os

import httpx

_BASE_URL = "https://a.klaviyo.com/api"


def _get_headers():
    """Return authorization headers for Klaviyo API.

    Requires: KLAVIYO_API_KEY
    """
    return {
        "Authorization": f"Klaviyo-API-Key {os.environ['KLAVIYO_API_KEY']}",
        "revision": "2024-10-15",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def klaviyo_campaigns(
    status: str | None = None,
) -> dict:
    """List Klaviyo email campaigns.

    Args:
        status: Optional filter — draft, scheduled, or sent. None returns all.

    Returns:
        Dict with 'campaigns' list. Each campaign contains id, name, status,
        send_time, and audience info.
    """
    headers = _get_headers()
    params = {}
    if status:
        params["filter"] = f"equals(messages.channel,'email'),equals(status,'{status}')"
    else:
        params["filter"] = "equals(messages.channel,'email')"

    resp = httpx.get(f"{_BASE_URL}/campaigns", headers=headers, params=params)
    data = resp.json().get("data", [])
    return {"campaigns": data}


def klaviyo_flows(
    status: str | None = None,
) -> dict:
    """List Klaviyo automation flows.

    Args:
        status: Optional filter — live, draft, or manual. None returns all.

    Returns:
        Dict with 'flows' list. Each flow contains id, name, status,
        trigger type, and action count.
    """
    headers = _get_headers()
    params = {}
    if status:
        params["filter"] = f"equals(status,'{status}')"

    resp = httpx.get(f"{_BASE_URL}/flows", headers=headers, params=params)
    data = resp.json().get("data", [])
    return {"flows": data}


def klaviyo_segments(
    name_filter: str | None = None,
) -> dict:
    """List Klaviyo audience segments.

    Args:
        name_filter: Optional substring to filter segment names. None returns all.

    Returns:
        Dict with 'segments' list. Each segment contains id, name,
        and profile count.
    """
    headers = _get_headers()
    resp = httpx.get(f"{_BASE_URL}/segments", headers=headers)
    data = resp.json().get("data", [])

    if name_filter:
        data = [
            s for s in data
            if name_filter.lower() in s.get("attributes", {}).get("name", "").lower()
        ]
    return {"segments": data}


def klaviyo_metrics(
    metric_id: str | None = None,
    date_range: str | None = None,
) -> dict:
    """Read Klaviyo metrics or metric aggregates.

    Args:
        metric_id: Optional metric ID for aggregation. None lists all metrics.
        date_range: Date range as 'YYYY-MM-DD,YYYY-MM-DD' for aggregates.
            Required when metric_id is provided.

    Returns:
        Dict with 'metrics' list — either metric definitions or aggregate data.
    """
    headers = _get_headers()

    if metric_id and date_range:
        start, end = date_range.split(",", 1)
        body = {
            "data": {
                "type": "metric-aggregate",
                "attributes": {
                    "metric_id": metric_id,
                    "measurements": ["count", "sum_value", "unique"],
                    "interval": "day",
                    "filter": [
                        f"greater-or-equal(datetime,{start.strip()}T00:00:00Z)",
                        f"less-than(datetime,{end.strip()}T23:59:59Z)",
                    ],
                },
            },
        }
        resp = httpx.post(
            f"{_BASE_URL}/metric-aggregates",
            headers=headers,
            json=body,
        )
        data = resp.json().get("data", {})
        return {"metrics": [data]}

    resp = httpx.get(f"{_BASE_URL}/metrics", headers=headers)
    data = resp.json().get("data", [])
    return {"metrics": data}


def klaviyo_profiles(
    segment_id: str | None = None,
    page_size: int = 20,
) -> dict:
    """List Klaviyo profiles, optionally filtered by segment.

    Args:
        segment_id: Optional segment ID to list profiles from that segment.
            None lists all profiles.
        page_size: Number of profiles per page (default 20, max 100).

    Returns:
        Dict with 'profiles' list and 'count' of returned profiles.
    """
    headers = _get_headers()
    params = {"page[size]": page_size}

    if segment_id:
        resp = httpx.get(
            f"{_BASE_URL}/segments/{segment_id}/profiles",
            headers=headers,
            params=params,
        )
    else:
        resp = httpx.get(f"{_BASE_URL}/profiles", headers=headers, params=params)

    data = resp.json().get("data", [])
    return {"profiles": data, "count": len(data)}


def klaviyo_catalogs(
    action: str = "list",
) -> dict:
    """List Klaviyo catalog items.

    Args:
        action: Action to perform — list (default). Returns catalog items
            synced from e-commerce platform.

    Returns:
        Dict with 'items' list. Each item contains id, title, price,
        and product URL.
    """
    headers = _get_headers()
    resp = httpx.get(f"{_BASE_URL}/catalog-items", headers=headers)
    data = resp.json().get("data", [])
    return {"items": data}

"""LinkedIn Ads API tools for D2C Growth role."""
import os

import httpx

_BASE_URL = "https://api.linkedin.com/rest"
_API_VERSION = "202402"  # LinkedIn API version YYYYMM format


def _get_headers():
    """Return LinkedIn API headers with auth and versioning.

    Requires: LINKEDIN_ADS_ACCESS_TOKEN
    """
    return {
        "Authorization": f"Bearer {os.environ['LINKEDIN_ADS_ACCESS_TOKEN']}",
        "Linkedin-Version": _API_VERSION,
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json",
    }


def _get_account_id():
    """Return the LinkedIn Ads account ID from environment.

    Requires: LINKEDIN_ADS_ACCOUNT_ID
    """
    return os.environ["LINKEDIN_ADS_ACCOUNT_ID"]


def _date_range_params(date_range: str) -> dict:
    """Convert a date_range shorthand to LinkedIn date range parameters."""
    mapping = {
        "last_7d": 7,
        "last_14d": 14,
        "last_30d": 30,
    }
    days = mapping.get(date_range, 7)
    from datetime import datetime, timedelta, timezone

    end = datetime.now(tz=timezone.utc).date()
    start = end - timedelta(days=days)
    return {
        "dateRange.start.year": start.year,
        "dateRange.start.month": start.month,
        "dateRange.start.day": start.day,
        "dateRange.end.year": end.year,
        "dateRange.end.month": end.month,
        "dateRange.end.day": end.day,
    }


def linkedin_ads_analytics(
    date_range: str = "last_7d",
    granularity: str = "DAILY",
    campaign_ids: list[str] | None = None,
) -> dict:
    """Read LinkedIn Ads analytics data with pivot by campaign.

    Args:
        date_range: Date range shorthand — last_7d, last_14d, or last_30d.
        granularity: Time granularity — DAILY or MONTHLY.
        campaign_ids: Optional list of campaign IDs to filter. None for all campaigns.

    Returns:
        Dict with 'rows' (list of analytics records), 'date_range', and 'granularity'.
        Metrics include impressions, clicks, costInLocalCurrency, conversions.
    """
    headers = _get_headers()
    account_id = _get_account_id()
    params = {
        "q": "analytics",
        "pivot": "CAMPAIGN",
        "timeGranularity": granularity,
        **_date_range_params(date_range),
    }
    if campaign_ids:
        for i, cid in enumerate(campaign_ids):
            params[f"campaigns[{i}]"] = f"urn:li:sponsoredCampaign:{cid}"
    else:
        params["accounts"] = f"urn:li:sponsoredAccount:{account_id}"

    resp = httpx.get(f"{_BASE_URL}/adAnalytics", headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()
    return {"rows": data.get("elements", []), "date_range": date_range, "granularity": granularity}


def linkedin_ads_campaigns(
    status: str | None = None,
) -> dict:
    """List LinkedIn Ads campaigns for the account.

    Args:
        status: Optional status filter — ACTIVE, PAUSED, ARCHIVED, DRAFT. None for all.

    Returns:
        Dict with 'campaigns' list. Each campaign contains id, name, status, objective.
    """
    headers = _get_headers()
    account_id = _get_account_id()
    params = {
        "q": "search",
        "search.account.values[0]": f"urn:li:sponsoredAccount:{account_id}",
    }
    if status:
        params["search.status.values[0]"] = status

    resp = httpx.get(f"{_BASE_URL}/adCampaigns", headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()
    return {"campaigns": data.get("elements", [])}


def linkedin_ads_create(
    campaign_name: str,
    objective: str,
    audience: dict,
    budget_daily: float,
) -> dict:
    """Create a new LinkedIn Ads campaign.

    Args:
        campaign_name: Name for the campaign (e.g. 'Vibe Bot - B2B Decision Makers').
        objective: Campaign objective — LEAD_GENERATION, WEBSITE_VISITS, BRAND_AWARENESS, etc.
        audience: Targeting spec dict (job_titles, company_sizes, industries, locations).
        budget_daily: Daily budget in USD (e.g. 100.0).

    Returns:
        Dict with 'campaign_id' of the newly created campaign. Created in PAUSED status.
    """
    headers = _get_headers()
    account_id = _get_account_id()
    body = {
        "account": f"urn:li:sponsoredAccount:{account_id}",
        "name": campaign_name,
        "objectiveType": objective,
        "status": "PAUSED",
        "dailyBudget": {"currencyCode": "USD", "amount": str(budget_daily)},
        "targetingCriteria": audience,
    }

    resp = httpx.post(f"{_BASE_URL}/adCampaigns", headers=headers, json=body)
    resp.raise_for_status()
    # LinkedIn returns the campaign ID in the x-restli-id header or response body
    campaign_id = resp.headers.get("x-restli-id", resp.json().get("id", "unknown"))
    return {"campaign_id": campaign_id}


def linkedin_ads_update(
    campaign_id: str,
    updates: dict,
) -> dict:
    """Update an existing LinkedIn Ads campaign (partial update).

    Args:
        campaign_id: The campaign ID to update.
        updates: Dict of fields to update (status, dailyBudget, name, etc.).

    Returns:
        Dict with 'updated' (True) and 'campaign_id'.
    """
    headers = _get_headers()
    resp = httpx.post(
        f"{_BASE_URL}/adCampaigns/{campaign_id}",
        headers={**headers, "X-Restli-Method": "PARTIAL_UPDATE"},
        json={"patch": {"$set": updates}},
    )
    resp.raise_for_status()
    return {"updated": True, "campaign_id": campaign_id}


def linkedin_ads_audiences(
    action: str = "list",
) -> dict:
    """List LinkedIn Ads audiences (Matched Audiences and DMP segments).

    Args:
        action: Action to perform — list (default). Returns saved audiences.

    Returns:
        Dict with 'audiences' list. Each audience contains id, name, and match count.
    """
    headers = _get_headers()
    account_id = _get_account_id()
    params = {
        "q": "account",
        "account": f"urn:li:sponsoredAccount:{account_id}",
    }

    resp = httpx.get(f"{_BASE_URL}/dmpSegments", headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()
    return {"audiences": data.get("elements", [])}


def linkedin_ads_conversions(
    date_range: str = "last_7d",
) -> dict:
    """Read LinkedIn Ads conversion tracking data.

    Args:
        date_range: Date range shorthand — last_7d, last_14d, or last_30d.

    Returns:
        Dict with 'conversions' (list of conversion records) and 'date_range'.
        Includes lead form completions, website conversions, and cost per conversion.
    """
    headers = _get_headers()
    account_id = _get_account_id()
    params = {
        "q": "analytics",
        "pivot": "CONVERSION",
        "timeGranularity": "DAILY",
        "accounts": f"urn:li:sponsoredAccount:{account_id}",
        **_date_range_params(date_range),
    }

    resp = httpx.get(f"{_BASE_URL}/adAnalytics", headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()
    return {"conversions": data.get("elements", []), "date_range": date_range}

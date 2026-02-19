"""Amazon Ads API tools for D2C Growth role."""
import gzip
import json
import os
import time

import httpx


def _get_client():
    """Initialize Amazon Ads API client credentials from environment.

    Requires: AMAZON_ADS_CLIENT_ID, AMAZON_ADS_CLIENT_SECRET, AMAZON_ADS_REFRESH_TOKEN,
              AMAZON_ADS_PROFILE_ID, AMAZON_ADS_REGION (default: NA)
    """
    credentials = {
        "refresh_token": os.environ["AMAZON_ADS_REFRESH_TOKEN"],
        "client_id": os.environ["AMAZON_ADS_CLIENT_ID"],
        "client_secret": os.environ["AMAZON_ADS_CLIENT_SECRET"],
        "profile_id": os.environ["AMAZON_ADS_PROFILE_ID"],
    }
    return credentials


def _get_profile_id() -> str:
    """Return the Amazon Ads profile ID from environment."""
    return os.environ["AMAZON_ADS_PROFILE_ID"]


def _request_report(credentials: dict, ad_product: str, report_type: str, columns: list[str], date_range: str) -> str:
    """Request an async report and return the report ID.

    Args:
        credentials: Amazon Ads API credentials dict.
        ad_product: SPONSORED_PRODUCTS, SPONSORED_BRANDS, or SPONSORED_DISPLAY.
        report_type: Report type — spSearchTerm, spCampaigns, sbCampaigns, etc.
        columns: List of metric/dimension column names to include.
        date_range: Date range — last_24h, last_7d, last_30d, or YYYY-MM-DD,YYYY-MM-DD.

    Returns:
        Report ID string for polling.
    """
    region_map = {
        "NA": "https://advertising-api.amazon.com",
        "EU": "https://advertising-api-eu.amazon.com",
        "FE": "https://advertising-api-fe.amazon.com",
    }
    region = os.environ.get("AMAZON_ADS_REGION", "NA")
    base_url = region_map.get(region, region_map["NA"])

    body = {
        "reportType": report_type,
        "columns": columns,
        "dateRange": date_range,
    }

    resp = httpx.post(
        f"{base_url}/reporting/reports",
        json=body,
        headers={
            "Amazon-Advertising-API-ClientId": credentials["client_id"],
            "Amazon-Advertising-API-Scope": credentials["profile_id"],
            "Authorization": f"Bearer {credentials['refresh_token']}",
            "Content-Type": "application/vnd.createasyncreportrequest.v3+json",
        },
    )
    resp.raise_for_status()
    return resp.json()["reportId"]


def _poll_report(credentials: dict, report_id: str, max_retries: int = 10, sleep_seconds: float = 5.0) -> str:
    """Poll until an async report completes, then return the download URL.

    Args:
        credentials: Amazon Ads API credentials dict.
        report_id: Report ID from _request_report.
        max_retries: Maximum number of poll attempts.
        sleep_seconds: Seconds to wait between polls.

    Returns:
        Download URL for the completed report.

    Raises:
        TimeoutError: If the report does not complete within max_retries.
    """
    region_map = {
        "NA": "https://advertising-api.amazon.com",
        "EU": "https://advertising-api-eu.amazon.com",
        "FE": "https://advertising-api-fe.amazon.com",
    }
    region = os.environ.get("AMAZON_ADS_REGION", "NA")
    base_url = region_map.get(region, region_map["NA"])

    for _ in range(max_retries):
        resp = httpx.get(
            f"{base_url}/reporting/reports/{report_id}",
            headers={
                "Amazon-Advertising-API-ClientId": credentials["client_id"],
                "Amazon-Advertising-API-Scope": credentials["profile_id"],
                "Authorization": f"Bearer {credentials['refresh_token']}",
            },
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") == "COMPLETED":
            return data["url"]
        time.sleep(sleep_seconds)

    raise TimeoutError(f"Report {report_id} did not complete after {max_retries} attempts")


def _download_report(credentials: dict, download_url: str) -> list[dict]:
    """Download and decompress a completed report.

    Args:
        credentials: Amazon Ads API credentials dict.
        download_url: URL returned by _poll_report.

    Returns:
        List of row dicts from the report.
    """
    resp = httpx.get(download_url)
    resp.raise_for_status()
    decompressed = gzip.decompress(resp.content)
    return json.loads(decompressed)


def amazon_ads_report(
    ad_product: str,
    report_type: str,
    columns: list[str],
    date_range: str,
) -> dict:
    """Request, poll, and download an Amazon Ads async report.

    This is the primary reporting interface. Amazon Ads uses an async 3-step flow:
    1. POST a report request to get a report ID.
    2. Poll the report status until COMPLETED.
    3. Download and decompress the gzip result.

    Args:
        ad_product: Ad product — SPONSORED_PRODUCTS, SPONSORED_BRANDS, or SPONSORED_DISPLAY.
        report_type: Report type — spSearchTerm, spCampaigns, sbCampaigns, sdCampaigns, etc.
        columns: List of metric/dimension columns (e.g. ['impressions', 'clicks', 'spend']).
        date_range: Date range — last_24h, last_7d, last_30d, or YYYY-MM-DD,YYYY-MM-DD.

    Returns:
        Dict with 'rows' (list of report row dicts), 'ad_product', and 'report_type'.
    """
    credentials = _get_client()
    report_id = _request_report(credentials, ad_product, report_type, columns, date_range)
    download_url = _poll_report(credentials, report_id)
    rows = _download_report(credentials, download_url)
    return {"rows": rows, "ad_product": ad_product, "report_type": report_type}


def amazon_ads_campaigns(
    ad_product: str = "SPONSORED_PRODUCTS",
    state: str | None = None,
) -> dict:
    """List Amazon Ads campaigns for a given ad product.

    Args:
        ad_product: Ad product — SPONSORED_PRODUCTS, SPONSORED_BRANDS, or SPONSORED_DISPLAY.
        state: Optional filter — enabled, paused, or archived.

    Returns:
        Dict with 'campaigns' (list of campaign dicts) and 'ad_product'.
    """
    credentials = _get_client()
    region_map = {
        "NA": "https://advertising-api.amazon.com",
        "EU": "https://advertising-api-eu.amazon.com",
        "FE": "https://advertising-api-fe.amazon.com",
    }
    region = os.environ.get("AMAZON_ADS_REGION", "NA")
    base_url = region_map.get(region, region_map["NA"])

    product_path = {
        "SPONSORED_PRODUCTS": "sp",
        "SPONSORED_BRANDS": "sb",
        "SPONSORED_DISPLAY": "sd",
    }
    path = product_path.get(ad_product, "sp")

    params = {}
    if state:
        params["stateFilter"] = state

    resp = httpx.get(
        f"{base_url}/v2/{path}/campaigns",
        params=params,
        headers={
            "Amazon-Advertising-API-ClientId": credentials["client_id"],
            "Amazon-Advertising-API-Scope": credentials["profile_id"],
            "Authorization": f"Bearer {credentials['refresh_token']}",
        },
    )
    resp.raise_for_status()
    return {"campaigns": resp.json(), "ad_product": ad_product}


def amazon_ads_keywords(
    campaign_id: str,
    ad_group_id: str | None = None,
) -> dict:
    """List keywords/targets for an Amazon Ads campaign.

    Args:
        campaign_id: Campaign ID to retrieve keywords for.
        ad_group_id: Optional ad group ID to narrow results.

    Returns:
        Dict with 'keywords' (list of keyword dicts) and 'campaign_id'.
    """
    credentials = _get_client()
    region_map = {
        "NA": "https://advertising-api.amazon.com",
        "EU": "https://advertising-api-eu.amazon.com",
        "FE": "https://advertising-api-fe.amazon.com",
    }
    region = os.environ.get("AMAZON_ADS_REGION", "NA")
    base_url = region_map.get(region, region_map["NA"])

    params = {"campaignIdFilter": campaign_id}
    if ad_group_id:
        params["adGroupIdFilter"] = ad_group_id

    resp = httpx.get(
        f"{base_url}/v2/sp/keywords",
        params=params,
        headers={
            "Amazon-Advertising-API-ClientId": credentials["client_id"],
            "Amazon-Advertising-API-Scope": credentials["profile_id"],
            "Authorization": f"Bearer {credentials['refresh_token']}",
        },
    )
    resp.raise_for_status()
    return {"keywords": resp.json(), "campaign_id": campaign_id}


def amazon_ads_bid_update(
    campaign_id: str,
    ad_group_id: str,
    keyword_id: str,
    new_bid: float,
) -> dict:
    """Update bid for an Amazon Ads keyword/target.

    Args:
        campaign_id: Campaign ID containing the keyword.
        ad_group_id: Ad group ID containing the keyword.
        keyword_id: Keyword ID to update.
        new_bid: New bid amount in USD.

    Returns:
        Dict with 'updated' (True), 'keyword_id', and 'new_bid'.
    """
    credentials = _get_client()
    region_map = {
        "NA": "https://advertising-api.amazon.com",
        "EU": "https://advertising-api-eu.amazon.com",
        "FE": "https://advertising-api-fe.amazon.com",
    }
    region = os.environ.get("AMAZON_ADS_REGION", "NA")
    base_url = region_map.get(region, region_map["NA"])

    body = [
        {
            "keywordId": int(keyword_id),
            "bid": new_bid,
        }
    ]

    resp = httpx.put(
        f"{base_url}/v2/sp/keywords",
        json=body,
        headers={
            "Amazon-Advertising-API-ClientId": credentials["client_id"],
            "Amazon-Advertising-API-Scope": credentials["profile_id"],
            "Authorization": f"Bearer {credentials['refresh_token']}",
            "Content-Type": "application/json",
        },
    )
    resp.raise_for_status()
    return {"updated": True, "keyword_id": keyword_id, "new_bid": new_bid}


def amazon_ads_budget(
    campaign_id: str,
    new_budget: float | None = None,
) -> dict:
    """Read or update daily budget for an Amazon Ads campaign.

    If new_budget is None, reads the current budget. Otherwise, updates it.

    Args:
        campaign_id: Campaign ID to read/update budget for.
        new_budget: New daily budget in USD, or None to read current.

    Returns:
        Dict with 'campaign_id', 'budget' (current value), and 'updated' (bool).
    """
    credentials = _get_client()
    region_map = {
        "NA": "https://advertising-api.amazon.com",
        "EU": "https://advertising-api-eu.amazon.com",
        "FE": "https://advertising-api-fe.amazon.com",
    }
    region = os.environ.get("AMAZON_ADS_REGION", "NA")
    base_url = region_map.get(region, region_map["NA"])

    headers = {
        "Amazon-Advertising-API-ClientId": credentials["client_id"],
        "Amazon-Advertising-API-Scope": credentials["profile_id"],
        "Authorization": f"Bearer {credentials['refresh_token']}",
    }

    if new_budget is None:
        resp = httpx.get(
            f"{base_url}/v2/sp/campaigns/{campaign_id}",
            headers=headers,
        )
        resp.raise_for_status()
        campaign_data = resp.json()
        return {
            "campaign_id": campaign_id,
            "budget": campaign_data.get("dailyBudget", 0.0),
            "updated": False,
        }

    body = [
        {
            "campaignId": int(campaign_id),
            "dailyBudget": new_budget,
        }
    ]
    resp = httpx.put(
        f"{base_url}/v2/sp/campaigns",
        json=body,
        headers={**headers, "Content-Type": "application/json"},
    )
    resp.raise_for_status()
    return {"campaign_id": campaign_id, "budget": new_budget, "updated": True}


def amazon_ads_search_terms(
    campaign_id: str,
    date_range: str = "last_7d",
) -> dict:
    """Get search term report for an Amazon Ads campaign.

    Convenience wrapper around amazon_ads_report that fetches search term data
    for a specific campaign with standard columns.

    Args:
        campaign_id: Campaign ID to pull search terms for.
        date_range: Date range — last_24h, last_7d, last_30d, or YYYY-MM-DD,YYYY-MM-DD.

    Returns:
        Dict with 'search_terms' (list of search term row dicts) and 'campaign_id'.
    """
    columns = [
        "searchTerm", "impressions", "clicks", "spend",
        "sales7d", "orders7d", "campaignId",
    ]
    result = amazon_ads_report(
        ad_product="SPONSORED_PRODUCTS",
        report_type="spSearchTerm",
        columns=columns,
        date_range=date_range,
    )
    # Filter rows for the requested campaign
    filtered = [
        row for row in result["rows"]
        if str(row.get("campaignId", "")) == str(campaign_id)
    ]
    return {"search_terms": filtered, "campaign_id": campaign_id}

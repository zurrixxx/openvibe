"""Meta Ads API tools for D2C Growth role."""
import os


def _get_account():
    """Initialize Meta Ads API client from environment.

    Requires: META_APP_ID, META_APP_SECRET, META_ACCESS_TOKEN, META_AD_ACCOUNT_ID
    """
    from facebook_business.api import FacebookAdsApi
    from facebook_business.adobjects.adaccount import AdAccount

    FacebookAdsApi.init(
        app_id=os.environ["META_APP_ID"],
        app_secret=os.environ["META_APP_SECRET"],
        access_token=os.environ["META_ACCESS_TOKEN"],
    )
    return AdAccount(f'act_{os.environ["META_AD_ACCOUNT_ID"]}')


_DEFAULT_FIELDS = [
    "campaign_name", "spend", "impressions", "clicks",
    "cpc", "cpm", "ctr", "actions", "cost_per_action_type",
]


def meta_ads_read(
    level: str = "campaign",
    date_range: str = "last_7d",
    fields: list[str] | None = None,
) -> dict:
    """Read Meta Ads performance data.

    Args:
        level: Reporting level — campaign, adset, or ad.
        date_range: Date range — last_24h, last_7d, last_30d, or YYYY-MM-DD,YYYY-MM-DD.
        fields: Metrics to retrieve (default: spend, impressions, clicks, cpc, cpm, ctr, actions).

    Returns:
        Dict with 'level', 'date_range', and 'rows' (list of performance records).
    """
    account = _get_account()
    report_fields = fields or _DEFAULT_FIELDS

    # Build date preset or time range
    params = {}
    if "," in date_range:
        start, end = date_range.split(",", 1)
        params["time_range"] = {"since": start.strip(), "until": end.strip()}
    else:
        params["date_preset"] = date_range

    rows = []
    if level == "campaign":
        for campaign in account.get_campaigns(fields=["name", "status"]):
            insights = campaign.get_insights(fields=report_fields, params=params)
            for row in insights:
                rows.append(dict(row))
    elif level == "adset":
        for adset in account.get_ad_sets(fields=["name", "status"]):
            insights = adset.get_insights(fields=report_fields, params=params)
            for row in insights:
                rows.append(dict(row))
    elif level == "ad":
        for ad in account.get_ads(fields=["name", "status"]):
            insights = ad.get_insights(fields=report_fields, params=params)
            for row in insights:
                rows.append(dict(row))

    return {"level": level, "date_range": date_range, "rows": rows}


def _create_adset(account, campaign_id: str, budget_daily: float, targeting: dict):
    """Create an adset under a campaign."""
    params = {
        "name": f"Adset - {campaign_id}",
        "campaign_id": campaign_id,
        "daily_budget": int(budget_daily * 100),  # cents
        "billing_event": "IMPRESSIONS",
        "optimization_goal": "OFFSITE_CONVERSIONS",
        "targeting": targeting,
        "status": "PAUSED",  # Start paused for review
    }
    return account.create_ad_set(fields=[], params=params)


def _create_ad(account, adset_id: str, creative: dict):
    """Create an ad under an adset."""
    params = {
        "name": f"Ad - {adset_id}",
        "adset_id": adset_id,
        "creative": creative,
        "status": "PAUSED",
    }
    return account.create_ad(fields=[], params=params)


def _get_object(object_type: str, object_id: str):
    """Get a Meta Ads object by type and ID."""
    from facebook_business.adobjects.campaign import Campaign
    from facebook_business.adobjects.adset import AdSet
    from facebook_business.adobjects.ad import Ad

    classes = {"campaign": Campaign, "adset": AdSet, "ad": Ad}
    cls = classes.get(object_type)
    if not cls:
        raise ValueError(f"Unknown object_type: {object_type}")
    return cls(object_id)


def meta_ads_create(
    campaign_name: str,
    objective: str,
    budget_daily: float,
    targeting: dict,
    creative: dict,
) -> dict:
    """Create a new Meta Ads campaign with adset and ad.

    Args:
        campaign_name: Name for the campaign (e.g. 'Bot - Foundation Test').
        objective: Campaign objective (OUTCOME_SALES, OUTCOME_TRAFFIC, etc.).
        budget_daily: Daily budget in USD.
        targeting: Audience targeting spec (age_min, age_max, interests, etc.).
        creative: Ad creative dict (headline, body, image_url, link).

    Returns:
        Dict with campaign_id, adset_id, and ad_id. All created in PAUSED status.
    """
    account = _get_account()

    campaign = account.create_campaign(fields=[], params={
        "name": campaign_name,
        "objective": objective,
        "status": "PAUSED",
        "special_ad_categories": [],
    })
    campaign_id = campaign["id"]

    adset = _create_adset(account, campaign_id, budget_daily, targeting)
    adset_id = adset["id"]

    ad = _create_ad(account, adset_id, creative)
    ad_id = ad["id"]

    return {"campaign_id": campaign_id, "adset_id": adset_id, "ad_id": ad_id}


def meta_ads_update(
    object_type: str,
    object_id: str,
    updates: dict,
) -> dict:
    """Update a Meta Ads object (campaign, adset, or ad).

    Args:
        object_type: Type — campaign, adset, or ad.
        object_id: ID of the object to update.
        updates: Fields to update (status, daily_budget, bid_amount, name, etc.).

    Returns:
        Dict with updated=True and the object_id.
    """
    obj = _get_object(object_type, object_id)
    obj.api_update(fields=[], params=updates)
    return {"updated": True, "object_id": object_id, "updates": updates}

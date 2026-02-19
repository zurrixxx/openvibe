"""Google Ads API tools for D2C Growth role."""
import os


def _get_client():
    """Initialize Google Ads API client from environment.

    Requires: GOOGLE_ADS_DEVELOPER_TOKEN, GOOGLE_ADS_CLIENT_ID, GOOGLE_ADS_CLIENT_SECRET,
              GOOGLE_ADS_REFRESH_TOKEN, GOOGLE_ADS_CUSTOMER_ID
    """
    from google.ads.googleads.client import GoogleAdsClient
    return GoogleAdsClient.load_from_dict({
        "developer_token": os.environ["GOOGLE_ADS_DEVELOPER_TOKEN"],
        "client_id": os.environ["GOOGLE_ADS_CLIENT_ID"],
        "client_secret": os.environ["GOOGLE_ADS_CLIENT_SECRET"],
        "refresh_token": os.environ["GOOGLE_ADS_REFRESH_TOKEN"],
        "login_customer_id": os.environ.get("GOOGLE_ADS_LOGIN_CUSTOMER_ID"),
        "use_proto_plus": True,
    })


def _get_customer_id():
    """Return the Google Ads customer ID from environment."""
    return os.environ["GOOGLE_ADS_CUSTOMER_ID"]


def google_ads_query(
    query: str,
    customer_id: str | None = None,
) -> dict:
    """Execute a GAQL (Google Ads Query Language) query.

    Args:
        query: A valid GAQL query string (e.g. 'SELECT campaign.name FROM campaign').
        customer_id: Google Ads customer ID. Defaults to GOOGLE_ADS_CUSTOMER_ID env var.

    Returns:
        Dict with 'rows' (list of result dicts) and 'query' (the executed query).
        Note: cost/budget values are in micros (1 USD = 1,000,000 micros).
    """
    client = _get_client()
    cid = customer_id or _get_customer_id()
    service = client.get_service("GoogleAdsService")
    response = service.search(customer_id=cid, query=query)
    rows = [dict(row) for row in response]
    return {"rows": rows, "query": query}


def google_ads_mutate(
    operations: list[dict],
    customer_id: str | None = None,
) -> dict:
    """Apply mutations (create, update, remove) to Google Ads resources.

    Args:
        operations: List of mutate operation dicts. Each dict should contain
            the resource type and operation details as expected by the Google Ads API.
        customer_id: Google Ads customer ID. Defaults to GOOGLE_ADS_CUSTOMER_ID env var.

    Returns:
        Dict with 'results' (list of resource name strings) and 'operation_count'.
    """
    client = _get_client()
    cid = customer_id or _get_customer_id()
    service = client.get_service("GoogleAdsService")
    response = service.mutate(customer_id=cid, mutate_operations=operations)
    results = [result.resource_name for result in response.mutate_operation_responses]
    return {"results": results, "operation_count": len(operations)}


def google_ads_budget(
    campaign_id: str,
    new_budget_micros: int | None = None,
    customer_id: str | None = None,
) -> dict:
    """Read or update a campaign budget.

    If new_budget_micros is None, reads the current budget. If provided, updates
    the campaign budget to the new value.

    Args:
        campaign_id: The campaign ID to read/update budget for.
        new_budget_micros: New budget in micros (1 USD = 1,000,000 micros). None to read only.
        customer_id: Google Ads customer ID. Defaults to GOOGLE_ADS_CUSTOMER_ID env var.

    Returns:
        Dict with 'campaign_id', 'budget_micros', and 'budget_usd'.
    """
    client = _get_client()
    cid = customer_id or _get_customer_id()
    service = client.get_service("GoogleAdsService")

    if new_budget_micros is None:
        query = (
            f"SELECT campaign.id, campaign_budget.amount_micros "
            f"FROM campaign WHERE campaign.id = {campaign_id}"
        )
        response = service.search(customer_id=cid, query=query)
        for row in response:
            micros = row.campaign_budget.amount_micros
            return {
                "campaign_id": campaign_id,
                "budget_micros": micros,
                "budget_usd": micros / 1_000_000,
            }
        return {"campaign_id": campaign_id, "budget_micros": 0, "budget_usd": 0.0}

    # Update budget
    budget_service = client.get_service("CampaignBudgetService")
    # First get the budget resource name
    query = (
        f"SELECT campaign.id, campaign.campaign_budget "
        f"FROM campaign WHERE campaign.id = {campaign_id}"
    )
    response = service.search(customer_id=cid, query=query)
    for row in response:
        budget_resource = row.campaign.campaign_budget
        budget_op = client.get_type("CampaignBudgetOperation")
        budget_op.update.resource_name = budget_resource
        budget_op.update.amount_micros = new_budget_micros
        client.copy_from(
            budget_op.update_mask,
            client.get_type("FieldMask")(paths=["amount_micros"]),
        )
        budget_service.mutate_campaign_budgets(
            customer_id=cid, operations=[budget_op]
        )
        return {
            "campaign_id": campaign_id,
            "budget_micros": new_budget_micros,
            "budget_usd": new_budget_micros / 1_000_000,
        }
    return {"campaign_id": campaign_id, "error": "Campaign not found"}


def google_ads_recommendations(
    customer_id: str | None = None,
) -> dict:
    """Read Google Ads optimization recommendations.

    Retrieves active recommendations such as keyword suggestions, bid adjustments,
    and budget changes that Google Ads generates for the account.

    Args:
        customer_id: Google Ads customer ID. Defaults to GOOGLE_ADS_CUSTOMER_ID env var.

    Returns:
        Dict with 'recommendations' list. Each recommendation contains type, impact,
        campaign, and resource_name.
    """
    client = _get_client()
    cid = customer_id or _get_customer_id()
    service = client.get_service("GoogleAdsService")
    query = (
        "SELECT recommendation.type, recommendation.impact, "
        "recommendation.campaign, recommendation.resource_name "
        "FROM recommendation "
        "WHERE recommendation.type IN ("
        "'KEYWORD', 'TEXT_AD', 'TARGET_CPA_OPT_IN', "
        "'MAXIMIZE_CONVERSIONS_OPT_IN', 'ENHANCED_CPC_OPT_IN', "
        "'MAXIMIZE_CLICKS_OPT_IN', 'OPTIMIZE_AD_ROTATION', "
        "'RESPONSIVE_SEARCH_AD', 'MARGINAL_ROI_CAMPAIGN_BUDGET'"
        ")"
    )
    response = service.search(customer_id=cid, query=query)
    recommendations = [dict(row) for row in response]
    return {"recommendations": recommendations}


def google_ads_conversions(
    date_range: str = "LAST_7_DAYS",
    customer_id: str | None = None,
) -> dict:
    """Read campaign-level conversion data.

    Args:
        date_range: Google Ads date range constant — LAST_7_DAYS, LAST_30_DAYS,
            THIS_MONTH, LAST_MONTH, etc.
        customer_id: Google Ads customer ID. Defaults to GOOGLE_ADS_CUSTOMER_ID env var.

    Returns:
        Dict with 'rows' (campaign conversion metrics) and 'date_range'.
        Cost values are in micros (1 USD = 1,000,000 micros).
    """
    client = _get_client()
    cid = customer_id or _get_customer_id()
    service = client.get_service("GoogleAdsService")
    query = (
        "SELECT campaign.id, campaign.name, "
        "metrics.conversions, metrics.conversions_value, "
        "metrics.cost_per_conversion, metrics.cost_micros, "
        "metrics.impressions, metrics.clicks "
        "FROM campaign "
        f"WHERE segments.date DURING {date_range}"
    )
    response = service.search(customer_id=cid, query=query)
    rows = [dict(row) for row in response]
    return {"rows": rows, "date_range": date_range}

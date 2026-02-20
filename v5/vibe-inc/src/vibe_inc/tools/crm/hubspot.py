"""HubSpot CRM tools for D2C Growth role."""
import os

import httpx

_BASE_URL = "https://api.hubapi.com"


def _get_headers():
    """Return authorization headers for HubSpot API.

    Requires: HUBSPOT_ACCESS_TOKEN
    """
    return {
        "Authorization": f"Bearer {os.environ['HUBSPOT_ACCESS_TOKEN']}",
        "Content-Type": "application/json",
    }


def hubspot_contact_get(
    email: str | None = None,
    contact_id: str | None = None,
) -> dict:
    """Look up a HubSpot contact by email or ID.

    Args:
        email: Email address to search for. Preferred lookup method.
        contact_id: HubSpot contact ID for direct lookup.

    Returns:
        Dict with 'contact' containing id, properties (email, firstname,
        lastname, company, lifecyclestage, hs_lead_status), and 'found' bool.
        If no match, returns {'contact': None, 'found': False}.
    """
    headers = _get_headers()

    if contact_id:
        resp = httpx.get(
            f"{_BASE_URL}/crm/v3/objects/contacts/{contact_id}",
            headers=headers,
            params={
                "properties": "email,firstname,lastname,company,lifecyclestage,hs_lead_status",
            },
        )
        data = resp.json()
        return {"contact": data, "found": True}

    if email:
        body = {
            "filterGroups": [
                {
                    "filters": [
                        {
                            "propertyName": "email",
                            "operator": "EQ",
                            "value": email,
                        },
                    ],
                },
            ],
            "properties": [
                "email", "firstname", "lastname", "company",
                "lifecyclestage", "hs_lead_status",
            ],
        }
        resp = httpx.post(
            f"{_BASE_URL}/crm/v3/objects/contacts/search",
            headers=headers,
            json=body,
        )
        results = resp.json().get("results", [])
        if results:
            return {"contact": results[0], "found": True}

    return {"contact": None, "found": False}


def hubspot_contact_update(
    contact_id: str,
    properties: dict,
) -> dict:
    """Update a HubSpot contact's properties.

    Args:
        contact_id: HubSpot contact ID to update.
        properties: Dict of property names to new values.
            Common: lifecyclestage, hs_lead_status, custom properties.

    Returns:
        Dict with 'updated' bool and 'contact' with updated properties.
    """
    headers = _get_headers()
    resp = httpx.patch(
        f"{_BASE_URL}/crm/v3/objects/contacts/{contact_id}",
        headers=headers,
        json={"properties": properties},
    )
    data = resp.json()
    return {"updated": True, "contact": data}


def hubspot_deals_list(
    contact_id: str,
) -> dict:
    """List deals associated with a HubSpot contact.

    Args:
        contact_id: HubSpot contact ID to look up deals for.

    Returns:
        Dict with 'deals' list (each with id and type) and 'count'.
    """
    headers = _get_headers()
    resp = httpx.get(
        f"{_BASE_URL}/crm/v3/objects/contacts/{contact_id}/associations/deals",
        headers=headers,
    )
    results = resp.json().get("results", [])
    return {"deals": results, "count": len(results)}

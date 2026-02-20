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

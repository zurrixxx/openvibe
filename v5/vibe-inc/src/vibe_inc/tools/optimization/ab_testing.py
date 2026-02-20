"""A/B testing tools via Convert.com REST API."""
import os

import httpx

_BASE_URL = "https://api.convert.com/api/v1"


def _get_headers():
    """Return authorization headers for Convert.com API.

    Requires: CONVERT_API_TOKEN
    """
    return {
        "Authorization": f"Bearer {os.environ['CONVERT_API_TOKEN']}",
        "Content-Type": "application/json",
    }


def _get_account_id():
    """Return Convert.com account ID from environment."""
    return os.environ["CONVERT_ACCOUNT_ID"]


def _get_project_id():
    """Return Convert.com project ID from environment."""
    return os.environ["CONVERT_PROJECT_ID"]


def ab_test_read(
    experiment_id: str | None = None,
    status: str | None = None,
) -> dict:
    """Read Convert.com A/B test experiments and their results.

    Args:
        experiment_id: Optional specific experiment to read. If None, lists all.
        status: Optional filter: active, paused, completed, draft.

    Returns:
        Dict with experiments list or single experiment detail with results.
    """
    account_id = _get_account_id()
    project_id = _get_project_id()
    if experiment_id:
        url = f"{_BASE_URL}/accounts/{account_id}/projects/{project_id}/experiences/{experiment_id}"
        resp = httpx.get(url, headers=_get_headers())
        data = resp.json()
        return {"experiment": data}
    else:
        url = f"{_BASE_URL}/accounts/{account_id}/projects/{project_id}/experiences"
        params = {}
        if status:
            params["status"] = status
        resp = httpx.get(url, headers=_get_headers(), params=params)
        data = resp.json()
        experiments = data if isinstance(data, list) else data.get("data", [])
        return {"experiments": experiments, "count": len(experiments)}


def ab_test_manage(
    experiment_id: str,
    action: str,
    **kwargs,
) -> dict:
    """Manage a Convert.com A/B test experiment (pause, activate, archive).

    Args:
        experiment_id: The Convert.com experiment ID.
        action: One of 'pause', 'activate', 'archive'.

    Returns:
        Dict with action result and experiment_id.
    """
    account_id = _get_account_id()
    project_id = _get_project_id()
    url = f"{_BASE_URL}/accounts/{account_id}/projects/{project_id}/experiences/{experiment_id}"
    status_map = {"pause": "paused", "activate": "active", "archive": "completed"}
    payload = {"status": status_map.get(action, action)}
    resp = httpx.patch(url, headers=_get_headers(), json=payload)
    data = resp.json()
    return {"action": action, "experiment_id": experiment_id, "result": data}

# HubSpot CRMOps Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add CRMOps as the 10th D2C Growth operator with 6 HubSpot API tools, 4 agent nodes, 4 LangGraph workflows, shared memory configs, and ~25 tests.

**Architecture:** New `tools/crm/hubspot.py` provides 6 httpx-based HubSpot API v3 tool functions. `CRMOps` operator uses `@agent_node` pattern with tool injection. 4 workflow factories follow existing `StateGraph` single-node pattern. Shared memory adds CRM routing rules and pipeline config.

**Tech Stack:** Python 3.13, httpx, HubSpot API v3 (REST), LangGraph, openvibe-sdk

**Design doc:** `v5/docs/plans/2026-02-20-hubspot-crm-ops-design.md`

---

## Phase 1: HubSpot Tools (Tasks 1-4)

### Task 1: Create `tools/crm/` package + `hubspot.py` scaffold with `hubspot_contact_get`

**Files:**
- Create: `v5/vibe-inc/src/vibe_inc/tools/crm/__init__.py`
- Create: `v5/vibe-inc/src/vibe_inc/tools/crm/hubspot.py`
- Create: `v5/vibe-inc/tests/test_hubspot_tools.py`

**Step 1: Write the test file with first 2 tests**

```python
# v5/vibe-inc/tests/test_hubspot_tools.py
from unittest.mock import patch, MagicMock


def _mock_response(json_data):
    """Create a mock httpx response with .json() returning given data."""
    resp = MagicMock()
    resp.json.return_value = json_data
    return resp


def test_hubspot_contact_get_by_email():
    """hubspot_contact_get searches by email and returns contact with enrichment info."""
    from vibe_inc.tools.crm.hubspot import hubspot_contact_get

    mock_resp = _mock_response({
        "results": [
            {
                "id": "501",
                "properties": {
                    "email": "buyer@acme.com",
                    "firstname": "Jane",
                    "lastname": "Doe",
                    "company": "Acme Corp",
                    "lifecyclestage": "customer",
                    "hs_lead_status": "OPEN",
                },
            },
        ],
    })

    with patch("vibe_inc.tools.crm.hubspot.httpx") as mock_httpx, \
         patch("vibe_inc.tools.crm.hubspot._get_headers", return_value={"Authorization": "Bearer test"}):
        mock_httpx.post.return_value = mock_resp
        result = hubspot_contact_get(email="buyer@acme.com")

    assert "contact" in result
    assert result["contact"]["id"] == "501"
    assert result["contact"]["properties"]["company"] == "Acme Corp"


def test_hubspot_contact_get_has_docstring():
    """Tool function must have a docstring for Anthropic schema generation."""
    from vibe_inc.tools.crm.hubspot import hubspot_contact_get
    assert hubspot_contact_get.__doc__ is not None
    assert "HubSpot" in hubspot_contact_get.__doc__
```

**Step 2: Run test to verify it fails**

Run: `cd v5/vibe-inc && pytest tests/test_hubspot_tools.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'vibe_inc.tools.crm'`

**Step 3: Create package init and implement `hubspot_contact_get`**

```python
# v5/vibe-inc/src/vibe_inc/tools/crm/__init__.py
```

```python
# v5/vibe-inc/src/vibe_inc/tools/crm/hubspot.py
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
```

**Step 4: Run test to verify it passes**

Run: `cd v5/vibe-inc && pytest tests/test_hubspot_tools.py -v`
Expected: 2 passed

**Step 5: Commit**

```bash
git add v5/vibe-inc/src/vibe_inc/tools/crm/ v5/vibe-inc/tests/test_hubspot_tools.py
git commit -m "feat(d2c-growth): add HubSpot tools package + hubspot_contact_get"
```

---

### Task 2: Add `hubspot_contact_update` + `hubspot_deals_list`

**Files:**
- Modify: `v5/vibe-inc/src/vibe_inc/tools/crm/hubspot.py`
- Modify: `v5/vibe-inc/tests/test_hubspot_tools.py`

**Step 1: Add 2 tests**

Append to `test_hubspot_tools.py`:

```python
def test_hubspot_contact_update_sends_patch():
    """hubspot_contact_update PATCHes contact properties."""
    from vibe_inc.tools.crm.hubspot import hubspot_contact_update

    mock_resp = _mock_response({
        "id": "501",
        "properties": {"lifecyclestage": "opportunity"},
    })

    with patch("vibe_inc.tools.crm.hubspot.httpx") as mock_httpx, \
         patch("vibe_inc.tools.crm.hubspot._get_headers", return_value={"Authorization": "Bearer test"}):
        mock_httpx.patch.return_value = mock_resp
        result = hubspot_contact_update(
            contact_id="501",
            properties={"lifecyclestage": "opportunity"},
        )

    assert result["updated"] is True
    assert result["contact"]["properties"]["lifecyclestage"] == "opportunity"
    mock_httpx.patch.assert_called_once()


def test_hubspot_deals_list_returns_deals():
    """hubspot_deals_list returns associated deals for a contact."""
    from vibe_inc.tools.crm.hubspot import hubspot_deals_list

    mock_assoc_resp = _mock_response({
        "results": [
            {"id": "deal_1", "type": "contact_to_deal"},
            {"id": "deal_2", "type": "contact_to_deal"},
        ],
    })

    with patch("vibe_inc.tools.crm.hubspot.httpx") as mock_httpx, \
         patch("vibe_inc.tools.crm.hubspot._get_headers", return_value={"Authorization": "Bearer test"}):
        mock_httpx.get.return_value = mock_assoc_resp
        result = hubspot_deals_list(contact_id="501")

    assert "deals" in result
    assert result["count"] == 2
```

**Step 2: Run test to verify it fails**

Run: `cd v5/vibe-inc && pytest tests/test_hubspot_tools.py::test_hubspot_contact_update_sends_patch tests/test_hubspot_tools.py::test_hubspot_deals_list_returns_deals -v`
Expected: FAIL with `ImportError: cannot import name 'hubspot_contact_update'`

**Step 3: Implement both functions**

Add to `hubspot.py`:

```python
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
```

**Step 4: Run test to verify it passes**

Run: `cd v5/vibe-inc && pytest tests/test_hubspot_tools.py -v`
Expected: 4 passed

**Step 5: Commit**

```bash
git add v5/vibe-inc/src/vibe_inc/tools/crm/hubspot.py v5/vibe-inc/tests/test_hubspot_tools.py
git commit -m "feat(d2c-growth): add hubspot_contact_update + hubspot_deals_list"
```

---

### Task 3: Add `hubspot_deal_create` + `hubspot_deal_update`

**Files:**
- Modify: `v5/vibe-inc/src/vibe_inc/tools/crm/hubspot.py`
- Modify: `v5/vibe-inc/tests/test_hubspot_tools.py`

**Step 1: Add 2 tests**

Append to `test_hubspot_tools.py`:

```python
def test_hubspot_deal_create_posts_with_association():
    """hubspot_deal_create creates deal and associates with contact."""
    from vibe_inc.tools.crm.hubspot import hubspot_deal_create

    mock_resp = _mock_response({
        "id": "deal_new",
        "properties": {
            "dealname": "Acme Corp - Bot",
            "dealstage": "lead",
            "pipeline": "b2b",
            "amount": "3000",
        },
    })

    with patch("vibe_inc.tools.crm.hubspot.httpx") as mock_httpx, \
         patch("vibe_inc.tools.crm.hubspot._get_headers", return_value={"Authorization": "Bearer test"}):
        mock_httpx.post.return_value = mock_resp
        result = hubspot_deal_create(
            contact_id="501",
            dealname="Acme Corp - Bot",
            pipeline="b2b",
            stage="lead",
            amount=3000,
        )

    assert result["created"] is True
    assert result["deal"]["id"] == "deal_new"
    assert mock_httpx.post.call_count == 2  # create deal + create association


def test_hubspot_deal_update_patches_stage():
    """hubspot_deal_update PATCHes deal properties."""
    from vibe_inc.tools.crm.hubspot import hubspot_deal_update

    mock_resp = _mock_response({
        "id": "deal_1",
        "properties": {"dealstage": "mql"},
    })

    with patch("vibe_inc.tools.crm.hubspot.httpx") as mock_httpx, \
         patch("vibe_inc.tools.crm.hubspot._get_headers", return_value={"Authorization": "Bearer test"}):
        mock_httpx.patch.return_value = mock_resp
        result = hubspot_deal_update(
            deal_id="deal_1",
            properties={"dealstage": "mql"},
        )

    assert result["updated"] is True
    assert result["deal"]["properties"]["dealstage"] == "mql"
```

**Step 2: Run test to verify it fails**

Run: `cd v5/vibe-inc && pytest tests/test_hubspot_tools.py::test_hubspot_deal_create_posts_with_association tests/test_hubspot_tools.py::test_hubspot_deal_update_patches_stage -v`
Expected: FAIL with `ImportError`

**Step 3: Implement both functions**

Add to `hubspot.py`:

```python
def hubspot_deal_create(
    contact_id: str,
    dealname: str,
    pipeline: str,
    stage: str,
    amount: float | None = None,
) -> dict:
    """Create a HubSpot deal and associate it with a contact.

    Args:
        contact_id: HubSpot contact ID to associate the deal with.
        dealname: Name for the deal (e.g. 'Acme Corp - Bot').
        pipeline: Pipeline ID (e.g. 'b2b').
        stage: Deal stage (e.g. 'lead', 'mql', 'sql').
        amount: Optional deal amount in dollars.

    Returns:
        Dict with 'created' bool and 'deal' with id and properties.
    """
    headers = _get_headers()
    properties = {
        "dealname": dealname,
        "pipeline": pipeline,
        "dealstage": stage,
    }
    if amount is not None:
        properties["amount"] = str(amount)

    resp = httpx.post(
        f"{_BASE_URL}/crm/v3/objects/deals",
        headers=headers,
        json={"properties": properties},
    )
    deal = resp.json()

    # Associate deal with contact
    httpx.post(
        f"{_BASE_URL}/crm/v3/objects/deals/{deal['id']}/associations/contacts/{contact_id}/deal_to_contact",
        headers=headers,
    )

    return {"created": True, "deal": deal}


def hubspot_deal_update(
    deal_id: str,
    properties: dict,
) -> dict:
    """Update a HubSpot deal's properties.

    Args:
        deal_id: HubSpot deal ID to update.
        properties: Dict of property names to new values.
            Common: dealstage, amount, closedate.

    Returns:
        Dict with 'updated' bool and 'deal' with updated properties.
    """
    headers = _get_headers()
    resp = httpx.patch(
        f"{_BASE_URL}/crm/v3/objects/deals/{deal_id}",
        headers=headers,
        json={"properties": properties},
    )
    data = resp.json()
    return {"updated": True, "deal": data}
```

**Step 4: Run test to verify it passes**

Run: `cd v5/vibe-inc && pytest tests/test_hubspot_tools.py -v`
Expected: 6 passed

**Step 5: Commit**

```bash
git add v5/vibe-inc/src/vibe_inc/tools/crm/hubspot.py v5/vibe-inc/tests/test_hubspot_tools.py
git commit -m "feat(d2c-growth): add hubspot_deal_create + hubspot_deal_update"
```

---

### Task 4: Add `hubspot_workflow_enroll`

**Files:**
- Modify: `v5/vibe-inc/src/vibe_inc/tools/crm/hubspot.py`
- Modify: `v5/vibe-inc/tests/test_hubspot_tools.py`

**Step 1: Add 2 tests**

Append to `test_hubspot_tools.py`:

```python
def test_hubspot_workflow_enroll_posts_enrollment():
    """hubspot_workflow_enroll POSTs contact enrollment to workflow."""
    from vibe_inc.tools.crm.hubspot import hubspot_workflow_enroll

    mock_resp = _mock_response({})
    mock_resp.status_code = 204

    with patch("vibe_inc.tools.crm.hubspot.httpx") as mock_httpx, \
         patch("vibe_inc.tools.crm.hubspot._get_headers", return_value={"Authorization": "Bearer test"}):
        mock_httpx.post.return_value = mock_resp
        result = hubspot_workflow_enroll(
            contact_email="buyer@acme.com",
            workflow_id="12345",
        )

    assert result["enrolled"] is True
    assert result["workflow_id"] == "12345"


def test_hubspot_workflow_enroll_has_docstring():
    """Tool function must have a docstring for Anthropic schema generation."""
    from vibe_inc.tools.crm.hubspot import hubspot_workflow_enroll
    assert hubspot_workflow_enroll.__doc__ is not None
    assert "HubSpot" in hubspot_workflow_enroll.__doc__
```

**Step 2: Run test to verify it fails**

Run: `cd v5/vibe-inc && pytest tests/test_hubspot_tools.py::test_hubspot_workflow_enroll_posts_enrollment tests/test_hubspot_tools.py::test_hubspot_workflow_enroll_has_docstring -v`
Expected: FAIL with `ImportError`

**Step 3: Implement `hubspot_workflow_enroll`**

Add to `hubspot.py`:

```python
def hubspot_workflow_enroll(
    contact_email: str,
    workflow_id: str,
) -> dict:
    """Enroll a contact into a HubSpot workflow.

    Args:
        contact_email: Email of the contact to enroll.
        workflow_id: HubSpot workflow (flow) ID to enroll the contact in.

    Returns:
        Dict with 'enrolled' bool, 'workflow_id', and 'contact_email'.
    """
    headers = _get_headers()
    resp = httpx.post(
        f"{_BASE_URL}/automation/v4/flows/{workflow_id}/enrollments",
        headers=headers,
        json={"objectId": contact_email, "objectType": "CONTACT"},
    )
    return {
        "enrolled": True,
        "workflow_id": workflow_id,
        "contact_email": contact_email,
    }
```

**Step 4: Run test to verify it passes**

Run: `cd v5/vibe-inc && pytest tests/test_hubspot_tools.py -v`
Expected: 8 passed

**Step 5: Commit**

```bash
git add v5/vibe-inc/src/vibe_inc/tools/crm/hubspot.py v5/vibe-inc/tests/test_hubspot_tools.py
git commit -m "feat(d2c-growth): add hubspot_workflow_enroll — all 6 HubSpot tools complete"
```

---

## Phase 2: CRMOps Operator (Tasks 5-6)

### Task 5: Create CRMOps operator with `workflow_trigger` + `deal_manage`

**Files:**
- Create: `v5/vibe-inc/src/vibe_inc/roles/d2c_growth/crm_ops.py`
- Create: `v5/vibe-inc/tests/test_crm_ops.py`

**Step 1: Write test file with 4 tests**

```python
# v5/vibe-inc/tests/test_crm_ops.py
from openvibe_sdk.llm import LLMResponse


def _text_response(content="done"):
    return LLMResponse(content=content, stop_reason="end_turn")


class FakeAgentLLM:
    """Fake LLM that returns pre-configured responses in sequence."""
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def call(self, *, system, messages, **kwargs):
        self.calls.append({"system": system, "messages": messages, **kwargs})
        return self.responses.pop(0)


# --- workflow_trigger ---

def test_workflow_trigger_is_agent_node():
    from vibe_inc.roles.d2c_growth.crm_ops import CRMOps
    assert hasattr(CRMOps.workflow_trigger, "_is_agent_node")
    assert CRMOps.workflow_trigger._is_agent_node is True
    assert "hubspot_workflow_enroll" in CRMOps.workflow_trigger._node_config["tools"]


def test_workflow_trigger_output_key():
    from vibe_inc.roles.d2c_growth.crm_ops import CRMOps

    llm = FakeAgentLLM([_text_response("Enrolled buyer@acme.com in b2b_onboarding")])
    op = CRMOps(llm=llm)
    result = op.workflow_trigger({"contact_email": "buyer@acme.com", "signal": "b2b_enriched"})

    assert "enrollment_result" in result


# --- deal_manage ---

def test_deal_manage_is_agent_node():
    from vibe_inc.roles.d2c_growth.crm_ops import CRMOps
    assert hasattr(CRMOps.deal_manage, "_is_agent_node")
    assert CRMOps.deal_manage._is_agent_node is True
    assert "hubspot_deal_create" in CRMOps.deal_manage._node_config["tools"]


def test_deal_manage_mentions_approval():
    from vibe_inc.roles.d2c_growth.crm_ops import CRMOps
    # The system prompt (docstring) should mention human approval for deal creation
    doc = CRMOps.deal_manage.__doc__
    assert "approval" in doc.lower() or "human" in doc.lower()
```

**Step 2: Run test to verify it fails**

Run: `cd v5/vibe-inc && pytest tests/test_crm_ops.py -v`
Expected: FAIL with `ModuleNotFoundError`

**Step 3: Implement CRMOps with first 2 nodes**

```python
# v5/vibe-inc/src/vibe_inc/roles/d2c_growth/crm_ops.py
"""CRMOps operator — manages HubSpot CRM operations for D2C Growth."""
from openvibe_sdk import Operator, agent_node

from vibe_inc.tools.crm.hubspot import (
    hubspot_contact_get,
    hubspot_contact_update,
    hubspot_deal_create,
    hubspot_deal_update,
    hubspot_deals_list,
    hubspot_workflow_enroll,
)
from vibe_inc.tools.shared_memory import read_memory, write_memory


class CRMOps(Operator):
    operator_id = "crm_ops"

    @agent_node(
        tools=[hubspot_contact_get, hubspot_workflow_enroll, read_memory],
        output_key="enrollment_result",
    )
    def workflow_trigger(self, state):
        """You are a HubSpot CRM workflow specialist for Vibe Inc.

        Given a signal and contact, enroll the contact in the correct HubSpot workflow:
        1. Look up the contact by email using hubspot_contact_get.
        2. Read routing rules from shared_memory (crm/routing_rules.yaml).
        3. Match the signal to the appropriate workflow:
           - high_value_d2c: order_total > $500 AND enrichment unknown → nurture_high_value
           - b2b_enriched: enrichment shows company with 50+ employees → b2b_onboarding
           - repeat_buyer: 2+ orders in 90 days → loyalty_program
        4. Enroll the contact using hubspot_workflow_enroll.
        5. Log the enrollment to shared_memory for audit trail.

        Return: enrollment confirmation with workflow name and contact details."""
        contact_email = state.get("contact_email", "")
        signal = state.get("signal", "")
        return f"Enroll {contact_email} based on signal: {signal}"

    @agent_node(
        tools=[hubspot_contact_get, hubspot_deals_list, hubspot_deal_create, hubspot_deal_update],
        output_key="deal_result",
    )
    def deal_manage(self, state):
        """You are a HubSpot deal management specialist for Vibe Inc.

        Manage B2B deals when enrichment signals are detected:
        1. Look up the contact and check enrichment data (company, size).
        2. Check if deals already exist for this contact using hubspot_deals_list.
        3. If B2B signal (company_size >= 50) and NO existing deal:
           - Prepare deal creation with pipeline=b2b, stage=lead.
           - Deal naming: [Company] - [Product] (e.g. 'Acme Corp - Bot').
           - NEW DEAL CREATION REQUIRES HUMAN APPROVAL. Present the deal details
             and wait for confirmation before calling hubspot_deal_create.
        4. If deal exists, evaluate stage advancement:
           - Stage advancement of 1 step (e.g. lead → mql): autonomous.
           - Skip-stage advancement (e.g. lead → sql): requires human approval.
        5. Update deal amount based on order value if applicable.

        Product deal values: Bot $3000, Dot $1500, Board $15000."""
        contact_id = state.get("contact_id", "")
        return f"Manage deals for contact: {contact_id}"
```

**Step 4: Run test to verify it passes**

Run: `cd v5/vibe-inc && pytest tests/test_crm_ops.py -v`
Expected: 4 passed

**Step 5: Commit**

```bash
git add v5/vibe-inc/src/vibe_inc/roles/d2c_growth/crm_ops.py v5/vibe-inc/tests/test_crm_ops.py
git commit -m "feat(d2c-growth): add CRMOps operator — workflow_trigger + deal_manage"
```

---

### Task 6: Add `contact_enrich_check` + `pipeline_review` nodes

**Files:**
- Modify: `v5/vibe-inc/src/vibe_inc/roles/d2c_growth/crm_ops.py`
- Modify: `v5/vibe-inc/tests/test_crm_ops.py`

**Step 1: Add 4 tests**

Append to `test_crm_ops.py`:

```python
# --- contact_enrich_check ---

def test_contact_enrich_check_is_agent_node():
    from vibe_inc.roles.d2c_growth.crm_ops import CRMOps
    assert hasattr(CRMOps.contact_enrich_check, "_is_agent_node")
    assert CRMOps.contact_enrich_check._is_agent_node is True
    assert "hubspot_contact_get" in CRMOps.contact_enrich_check._node_config["tools"]


def test_contact_enrich_check_output_key():
    from vibe_inc.roles.d2c_growth.crm_ops import CRMOps

    llm = FakeAgentLLM([_text_response("Contact enriched: Acme Corp, 200 employees")])
    op = CRMOps(llm=llm)
    result = op.contact_enrich_check({"contact_email": "buyer@acme.com"})

    assert "enrichment_result" in result


# --- pipeline_review ---

def test_pipeline_review_is_agent_node():
    from vibe_inc.roles.d2c_growth.crm_ops import CRMOps
    assert hasattr(CRMOps.pipeline_review, "_is_agent_node")
    assert CRMOps.pipeline_review._is_agent_node is True
    assert "hubspot_deals_list" in CRMOps.pipeline_review._node_config["tools"]


def test_pipeline_review_output_key():
    from vibe_inc.roles.d2c_growth.crm_ops import CRMOps

    llm = FakeAgentLLM([_text_response("Pipeline: 5 leads, 3 MQL, 1 SQL, $45K total")])
    op = CRMOps(llm=llm)
    result = op.pipeline_review({"pipeline_id": "b2b"})

    assert "pipeline_result" in result
```

**Step 2: Run test to verify it fails**

Run: `cd v5/vibe-inc && pytest tests/test_crm_ops.py::test_contact_enrich_check_is_agent_node tests/test_crm_ops.py::test_pipeline_review_is_agent_node -v`
Expected: FAIL with `AttributeError`

**Step 3: Add 2 nodes to CRMOps**

Append to `CRMOps` class in `crm_ops.py`:

```python
    @agent_node(
        tools=[hubspot_contact_get, read_memory],
        output_key="enrichment_result",
    )
    def contact_enrich_check(self, state):
        """You are a HubSpot contact enrichment analyst for Vibe Inc.

        Look up a contact and assess their enrichment status:
        1. Search by email using hubspot_contact_get.
        2. Report enrichment status:
           - ENRICHED: company, company size, industry, job title populated.
           - PARTIAL: some company fields populated but incomplete.
           - UNKNOWN: no company data — likely pure D2C consumer.
        3. If enriched, report: company name, employee count, industry, lifecycle stage.
        4. Check associated deals — report deal count and stages.
        5. Flag if contact has been in 'unknown' enrichment for >7 days
           (check hs_analytics_first_timestamp vs current date).
        6. Recommend action: move to B2B pipeline? Enroll in nurture? Suppress?

        Return: enrichment status, company details, deal associations, recommendation."""
        contact_email = state.get("contact_email", "")
        return f"Check enrichment for: {contact_email}"

    @agent_node(
        tools=[hubspot_deals_list, hubspot_contact_get, read_memory],
        output_key="pipeline_result",
    )
    def pipeline_review(self, state):
        """You are a HubSpot pipeline health analyst for Vibe Inc.

        Review deal pipeline health and flag issues:
        1. Read pipeline config from shared_memory (crm/pipeline_config.yaml).
        2. List deals by stage. For each stage, count deals and sum amounts.
        3. Flag stale deals: no stage change in 14+ days (per pipeline_config threshold).
        4. Calculate stage conversion rates: lead→mql, mql→sql, sql→proposal, proposal→close.
        5. Compare close rate against target (15% per pipeline_config).
        6. Product breakdown: separate Bot, Dot, Board deal values.
        7. Calculate average cycle time by product vs targets:
           - Bot: target 45 days
           - Dot: target 30 days
           - Board: target 90 days

        Format as progressive disclosure: headline KPIs → stage breakdown → stale alerts."""
        pipeline_id = state.get("pipeline_id", "default")
        return f"Review pipeline: {pipeline_id}"
```

**Step 4: Run test to verify it passes**

Run: `cd v5/vibe-inc && pytest tests/test_crm_ops.py -v`
Expected: 8 passed

**Step 5: Commit**

```bash
git add v5/vibe-inc/src/vibe_inc/roles/d2c_growth/crm_ops.py v5/vibe-inc/tests/test_crm_ops.py
git commit -m "feat(d2c-growth): add contact_enrich_check + pipeline_review to CRMOps"
```

---

## Phase 3: Workflows (Tasks 7-8)

### Task 7: Create CRM workflow factories

**Files:**
- Create: `v5/vibe-inc/src/vibe_inc/roles/d2c_growth/crm_workflows.py`
- Create: `v5/vibe-inc/tests/test_crm_workflows.py`

**Step 1: Write test file with 4 tests**

```python
# v5/vibe-inc/tests/test_crm_workflows.py
from openvibe_sdk.llm import LLMResponse


class FakeLLM:
    def call(self, *, system, messages, **kwargs):
        return LLMResponse(content="done")


def test_workflow_enrollment_graph_compiles():
    from vibe_inc.roles.d2c_growth.crm_workflows import create_workflow_enrollment_graph
    from vibe_inc.roles.d2c_growth.crm_ops import CRMOps

    op = CRMOps(llm=FakeLLM())
    graph = create_workflow_enrollment_graph(op)
    assert graph is not None


def test_deal_progression_graph_compiles():
    from vibe_inc.roles.d2c_growth.crm_workflows import create_deal_progression_graph
    from vibe_inc.roles.d2c_growth.crm_ops import CRMOps

    op = CRMOps(llm=FakeLLM())
    graph = create_deal_progression_graph(op)
    assert graph is not None


def test_enrichment_audit_graph_compiles():
    from vibe_inc.roles.d2c_growth.crm_workflows import create_enrichment_audit_graph
    from vibe_inc.roles.d2c_growth.crm_ops import CRMOps

    op = CRMOps(llm=FakeLLM())
    graph = create_enrichment_audit_graph(op)
    assert graph is not None


def test_pipeline_health_graph_compiles():
    from vibe_inc.roles.d2c_growth.crm_workflows import create_pipeline_health_graph
    from vibe_inc.roles.d2c_growth.crm_ops import CRMOps

    op = CRMOps(llm=FakeLLM())
    graph = create_pipeline_health_graph(op)
    assert graph is not None
```

**Step 2: Run test to verify it fails**

Run: `cd v5/vibe-inc && pytest tests/test_crm_workflows.py -v`
Expected: FAIL with `ModuleNotFoundError`

**Step 3: Implement workflow factories**

```python
# v5/vibe-inc/src/vibe_inc/roles/d2c_growth/crm_workflows.py
"""LangGraph workflow factories for CRMOps."""
from typing import TypedDict

from langgraph.graph import StateGraph


class WorkflowEnrollmentState(TypedDict, total=False):
    contact_email: str
    signal: str
    enrollment_result: str


class DealProgressionState(TypedDict, total=False):
    contact_id: str
    deal_data: dict
    deal_result: str


class EnrichmentAuditState(TypedDict, total=False):
    contact_email: str
    enrichment_result: str


class PipelineHealthState(TypedDict, total=False):
    pipeline_id: str
    pipeline_result: str


def create_workflow_enrollment_graph(operator):
    """CRM workflow enrollment: signal → contact lookup → workflow enroll."""
    graph = StateGraph(WorkflowEnrollmentState)
    graph.add_node("trigger", operator.workflow_trigger)
    graph.set_entry_point("trigger")
    graph.set_finish_point("trigger")
    return graph.compile()


def create_deal_progression_graph(operator):
    """CRM deal progression: contact → enrichment check → deal create/update."""
    graph = StateGraph(DealProgressionState)
    graph.add_node("manage", operator.deal_manage)
    graph.set_entry_point("manage")
    graph.set_finish_point("manage")
    return graph.compile()


def create_enrichment_audit_graph(operator):
    """CRM enrichment audit: contact → enrichment status → recommendation."""
    graph = StateGraph(EnrichmentAuditState)
    graph.add_node("check", operator.contact_enrich_check)
    graph.set_entry_point("check")
    graph.set_finish_point("check")
    return graph.compile()


def create_pipeline_health_graph(operator):
    """CRM pipeline health: deals → stage counts → stale alerts → KPIs."""
    graph = StateGraph(PipelineHealthState)
    graph.add_node("review", operator.pipeline_review)
    graph.set_entry_point("review")
    graph.set_finish_point("review")
    return graph.compile()
```

**Step 4: Run test to verify it passes**

Run: `cd v5/vibe-inc && pytest tests/test_crm_workflows.py -v`
Expected: 4 passed

**Step 5: Commit**

```bash
git add v5/vibe-inc/src/vibe_inc/roles/d2c_growth/crm_workflows.py v5/vibe-inc/tests/test_crm_workflows.py
git commit -m "feat(d2c-growth): add CRM workflow factories — 4 LangGraph graphs"
```

---

### Task 8: Create shared memory CRM config files + bootstrap tests

**Files:**
- Create: `v5/vibe-inc/shared_memory/crm/routing_rules.yaml`
- Create: `v5/vibe-inc/shared_memory/crm/pipeline_config.yaml`
- Create: `v5/vibe-inc/tests/test_crm_shared_memory.py`

**Step 1: Write test file with 3 tests**

```python
# v5/vibe-inc/tests/test_crm_shared_memory.py
import yaml
from pathlib import Path

_SHARED = Path(__file__).parent.parent / "shared_memory" / "crm"


def test_routing_rules_exists_and_has_signals():
    assert (_SHARED / "routing_rules.yaml").exists()
    data = yaml.safe_load((_SHARED / "routing_rules.yaml").read_text())
    assert "signals" in data
    assert "high_value_d2c" in data["signals"]
    assert "b2b_enriched" in data["signals"]
    assert "repeat_buyer" in data["signals"]
    # Each signal must have condition + workflow_id
    for signal_name, signal in data["signals"].items():
        assert "condition" in signal, f"{signal_name} missing condition"
        assert "workflow_id" in signal, f"{signal_name} missing workflow_id"


def test_pipeline_config_exists_and_has_stages():
    assert (_SHARED / "pipeline_config.yaml").exists()
    data = yaml.safe_load((_SHARED / "pipeline_config.yaml").read_text())
    assert "pipelines" in data
    assert "b2b" in data["pipelines"]
    b2b = data["pipelines"]["b2b"]
    assert "stages" in b2b
    assert "lead" in b2b["stages"]
    assert "closed_won" in b2b["stages"]
    assert b2b["stale_threshold_days"] == 14


def test_pipeline_config_has_product_targets():
    data = yaml.safe_load((_SHARED / "pipeline_config.yaml").read_text())
    assert "products" in data
    assert "bot" in data["products"]
    assert "dot" in data["products"]
    assert "board" in data["products"]
    assert data["products"]["bot"]["avg_deal_value"] == 3000
    assert data["products"]["board"]["typical_cycle_days"] == 90
```

**Step 2: Run test to verify it fails**

Run: `cd v5/vibe-inc && pytest tests/test_crm_shared_memory.py -v`
Expected: FAIL with `AssertionError` (files don't exist)

**Step 3: Create the YAML files**

```yaml
# v5/vibe-inc/shared_memory/crm/routing_rules.yaml
# CRM workflow routing rules — maps signals to HubSpot workflows.
# Used by CRMOps.workflow_trigger to determine enrollment targets.

signals:
  high_value_d2c:
    condition: "order_total > $500 AND enrichment_status = unknown"
    workflow_id: "nurture_high_value"
    description: "High-value D2C buyer not yet enriched — nurture for upsell"

  b2b_enriched:
    condition: "enrichment_status = enriched AND company_size >= 50"
    workflow_id: "b2b_onboarding"
    description: "Enrichment reveals B2B buyer — route to sales pipeline"

  repeat_buyer:
    condition: "order_count >= 2 AND days_since_last < 90"
    workflow_id: "loyalty_program"
    description: "Repeat purchaser within 90 days — loyalty nurture"
```

```yaml
# v5/vibe-inc/shared_memory/crm/pipeline_config.yaml
# B2B deal pipeline configuration for HubSpot CRM.
# Used by CRMOps.deal_manage and CRMOps.pipeline_review.

pipelines:
  b2b:
    stages:
      - lead
      - mql
      - sql
      - proposal
      - closed_won
      - closed_lost
    stale_threshold_days: 14
    target_close_rate: 0.15

products:
  bot:
    avg_deal_value: 3000
    typical_cycle_days: 45
  dot:
    avg_deal_value: 1500
    typical_cycle_days: 30
  board:
    avg_deal_value: 15000
    typical_cycle_days: 90
```

**Step 4: Run test to verify it passes**

Run: `cd v5/vibe-inc && pytest tests/test_crm_shared_memory.py -v`
Expected: 3 passed

**Step 5: Commit**

```bash
git add v5/vibe-inc/shared_memory/crm/ v5/vibe-inc/tests/test_crm_shared_memory.py
git commit -m "feat(d2c-growth): add CRM shared memory — routing rules + pipeline config"
```

---

## Phase 4: Wiring + Integration (Tasks 9-11)

### Task 9: Wire CRMOps into D2CGrowth role + main.py runtime

**Files:**
- Modify: `v5/vibe-inc/src/vibe_inc/roles/d2c_growth/__init__.py`
- Modify: `v5/vibe-inc/src/vibe_inc/main.py`
- Modify: `v5/vibe-inc/tests/test_d2c_growth.py`

**Step 1: Update role test to expect 10 operators**

In `test_d2c_growth.py`, find `test_d2c_growth_has_operators` and add:

```python
    assert "crm_ops" in op_ids
```

Also find `test_d2c_growth_has_operators` — the existing test already lists 9 operator IDs. Add `crm_ops` to the assertions.

**Step 2: Run test to verify it fails**

Run: `cd v5/vibe-inc && pytest tests/test_d2c_growth.py::test_d2c_growth_has_operators -v`
Expected: FAIL with `AssertionError: assert 'crm_ops' in op_ids`

**Step 3: Wire CRMOps into role**

In `v5/vibe-inc/src/vibe_inc/roles/d2c_growth/__init__.py`:
- Add import: `from .crm_ops import CRMOps`
- Add `CRMOps` to the `operators` list (10th entry)

In `v5/vibe-inc/src/vibe_inc/main.py`:
- Add imports for CRM workflow factories:
  ```python
  from vibe_inc.roles.d2c_growth.crm_workflows import (
      create_workflow_enrollment_graph,
      create_deal_progression_graph,
      create_enrichment_audit_graph,
      create_pipeline_health_graph,
  )
  ```
- Add 4 workflow registrations after CrossPlatformOps section:
  ```python
  # CRMOps workflows
  runtime.register_workflow("crm_ops", "workflow_enrollment", create_workflow_enrollment_graph)
  runtime.register_workflow("crm_ops", "deal_progression", create_deal_progression_graph)
  runtime.register_workflow("crm_ops", "enrichment_audit", create_enrichment_audit_graph)
  runtime.register_workflow("crm_ops", "pipeline_health", create_pipeline_health_graph)
  ```

**Step 4: Run test to verify it passes**

Run: `cd v5/vibe-inc && pytest tests/test_d2c_growth.py -v`
Expected: all pass, including `crm_ops` in operator list

**Step 5: Commit**

```bash
git add v5/vibe-inc/src/vibe_inc/roles/d2c_growth/__init__.py v5/vibe-inc/src/vibe_inc/main.py v5/vibe-inc/tests/test_d2c_growth.py
git commit -m "feat(d2c-growth): wire CRMOps into role + runtime — 10 operators, 48 workflows"
```

---

### Task 10: Add CRMOps integration tests

**Files:**
- Modify: `v5/vibe-inc/tests/test_integration_dataops_growth.py`

**Step 1: Add 4 integration tests + update operator count assertion**

Append to `test_integration_dataops_growth.py` before the runtime structure tests section:

```python
# --- CRMOps workflows ---


def test_crm_workflow_enrollment_activates():
    """CRMOps workflow_enrollment workflow runs through runtime."""
    runtime = _runtime()
    result = runtime.activate(
        role_id="d2c_growth",
        operator_id="crm_ops",
        workflow_id="workflow_enrollment",
        input_data={"contact_email": "buyer@acme.com", "signal": "b2b_enriched"},
    )
    assert "enrollment_result" in result


def test_crm_deal_progression_activates():
    """CRMOps deal_progression workflow runs through runtime."""
    runtime = _runtime()
    result = runtime.activate(
        role_id="d2c_growth",
        operator_id="crm_ops",
        workflow_id="deal_progression",
        input_data={"contact_id": "501"},
    )
    assert "deal_result" in result


def test_crm_enrichment_audit_activates():
    """CRMOps enrichment_audit workflow runs through runtime."""
    runtime = _runtime()
    result = runtime.activate(
        role_id="d2c_growth",
        operator_id="crm_ops",
        workflow_id="enrichment_audit",
        input_data={"contact_email": "buyer@acme.com"},
    )
    assert "enrichment_result" in result


def test_crm_pipeline_health_activates():
    """CRMOps pipeline_health workflow runs through runtime."""
    runtime = _runtime()
    result = runtime.activate(
        role_id="d2c_growth",
        operator_id="crm_ops",
        workflow_id="pipeline_health",
        input_data={"pipeline_id": "b2b"},
    )
    assert "pipeline_result" in result
```

Also update `test_runtime_d2c_growth_operator_count`:

Change assertion from `assert len(d2c.operators) >= 8` to `assert len(d2c.operators) >= 10`.

**Step 2: Run test to verify new tests pass**

Run: `cd v5/vibe-inc && pytest tests/test_integration_dataops_growth.py -v`
Expected: all pass (22 total — 18 existing + 4 new)

**Step 3: Commit**

```bash
git add v5/vibe-inc/tests/test_integration_dataops_growth.py
git commit -m "test(d2c-growth): add CRMOps integration tests — 4 workflow activations"
```

---

### Task 11: Run full suite + update PROGRESS.md

**Files:**
- Modify: `PROGRESS.md`

**Step 1: Run full vibe-inc test suite**

Run: `cd v5/vibe-inc && pytest tests/ -v`
Expected: ~329 passed (304 existing + ~25 new)

**Step 2: Update PROGRESS.md**

Update the vibe-inc test count in the table. Add CRMOps to the operator table. Update total test count. Add this plan to the Key Docs section.

**Step 3: Commit**

```bash
git add PROGRESS.md
git commit -m "docs: update PROGRESS.md — CRMOps complete, 10 operators, 48 workflows"
```

**Step 4: Push**

```bash
git push origin main
```

# HubSpot CRMOps Design

> New `CRMOps` operator under D2C Growth — surgical CRM operations via HubSpot API.

## Context

Vibe Inc syncs all Shopify orders into HubSpot. Enrichment reveals 30-40% of D2C customers are actually B2B buyers. HubSpot is the unified CRM for both D2C and B2B contacts, managing lifecycle stages, deal pipelines, and workflow automation.

Aggregate analytics already flow through Redshift (dbt-cdp sync). HubSpot API integration is for **single-record operations and workflow triggers** that can't be done through the warehouse.

## Data Flow

```
Shopify orders ──sync──→ HubSpot (all contacts)
                              │
                         Enrichment (30-40% → B2B)
                              │
                    ┌─────────┴──────────┐
                    │                    │
              B2B contacts          D2C contacts
              (deal pipeline,       (lifecycle email,
               sales team)          repeat purchase)
                    │                    │
                    └─────────┬──────────┘
                              │
                         Redshift (aggregate analytics)
```

## 1. Tools: `tools/crm/hubspot.py`

6 functions, httpx, HubSpot API v3. Auth: `HUBSPOT_ACCESS_TOKEN` env var.

| Tool | HTTP | Endpoint | Purpose |
|------|------|----------|---------|
| `hubspot_contact_get` | POST | `/crm/v3/objects/contacts/search` | Lookup by email or ID; returns enrichment status, company, lifecycle stage |
| `hubspot_contact_update` | PATCH | `/crm/v3/objects/contacts/{id}` | Update lifecycle stage, custom properties |
| `hubspot_deal_create` | POST | `/crm/v3/objects/deals` + association | Create deal linked to contact; set pipeline + stage |
| `hubspot_deal_update` | PATCH | `/crm/v3/objects/deals/{id}` | Move deal stage, update amount/properties |
| `hubspot_deals_list` | GET | `/crm/v3/objects/contacts/{id}/associations/deals` | List deals for a contact |
| `hubspot_workflow_enroll` | POST | `/automation/v4/flows/{id}/enrollments` | Enroll contact into a HubSpot workflow |

Pattern: private `_get_headers()` / `_get_client()` helpers, same as all other tool files.

## 2. Operator: `CRMOps`

File: `roles/d2c_growth/crm_ops.py` — 10th operator in D2C Growth.

### 2.1 `workflow_trigger` (priority 1)

- **Tools:** `hubspot_contact_get`, `hubspot_workflow_enroll`, `read_memory`
- **Output key:** `enrollment_result`
- **System prompt:** Given a signal (high-value D2C, B2B enriched, repeat buyer), look up the contact, check routing rules in shared_memory, enroll in the correct workflow. Log enrollment to shared_memory.

### 2.2 `deal_manage` (priority 2)

- **Tools:** `hubspot_contact_get`, `hubspot_deals_list`, `hubspot_deal_create`, `hubspot_deal_update`
- **Output key:** `deal_result`
- **System prompt:** When B2B signal detected (enrichment shows company with 50+ employees), check if deal exists. If not, create one in B2B pipeline. If exists, evaluate stage advancement. Deal creation requires human approval. Stage advancement <=1 step: autonomous.
- **Escalation:** New deal creation → human approval.

### 2.3 `contact_enrich_check` (priority 3)

- **Tools:** `hubspot_contact_get`, `read_memory`
- **Output key:** `enrichment_result`
- **System prompt:** Look up contact, report enrichment status (enriched/pending/unknown), company info if available, lifecycle stage, associated deals. Flag if contact has been in 'unknown' enrichment for >7 days.

### 2.4 `pipeline_review`

- **Tools:** `hubspot_deals_list`, `hubspot_contact_get`, `read_memory`
- **Output key:** `pipeline_result`
- **System prompt:** Review deal pipeline health. Flag stale deals (no stage change in 14+ days). Summarize pipeline by stage with total deal value. Compare close rates against benchmarks.

## 3. Workflows

File: `roles/d2c_growth/crm_workflows.py` — 4 LangGraph StateGraph factories.

| Workflow | State Fields | Factory |
|----------|-------------|---------|
| `workflow_enrollment` | `contact_email`, `signal`, `enrollment_result` | `create_workflow_enrollment_graph` |
| `deal_progression` | `contact_id`, `deal_data`, `deal_result` | `create_deal_progression_graph` |
| `enrichment_audit` | `contact_email`, `enrichment_result` | `create_enrichment_audit_graph` |
| `pipeline_health` | `pipeline_id`, `pipeline_result` | `create_pipeline_health_graph` |

## 4. Shared Memory

### `shared_memory/crm/routing_rules.yaml`

```yaml
signals:
  high_value_d2c:
    condition: "order_total > $500 AND enrichment_status = unknown"
    workflow_id: "nurture_high_value"
  b2b_enriched:
    condition: "enrichment_status = enriched AND company_size >= 50"
    workflow_id: "b2b_onboarding"
  repeat_buyer:
    condition: "order_count >= 2 AND days_since_last < 90"
    workflow_id: "loyalty_program"
```

### `shared_memory/crm/pipeline_config.yaml`

```yaml
pipelines:
  b2b:
    stages: [lead, mql, sql, proposal, closed_won, closed_lost]
    stale_threshold_days: 14
    target_close_rate: 0.15
products:
  bot: { avg_deal_value: 3000, typical_cycle_days: 45 }
  dot: { avg_deal_value: 1500, typical_cycle_days: 30 }
  board: { avg_deal_value: 15000, typical_cycle_days: 90 }
```

## 5. Wiring

- `D2CGrowth.__init__.py` — add `CRMOps` as 10th operator
- `main.py` — 4 new `register_workflow("crm_ops", ...)` calls (total: 48 workflows)
- `pyproject.toml` — no new deps (httpx already present)

## 6. Tests (~25 new)

| File | Count | What |
|------|-------|------|
| `test_hubspot_tools.py` | 8 | Mock httpx, verify request/response per tool |
| `test_crm_ops.py` | 8 | FakeAgentLLM, agent_node metadata + invocations |
| `test_crm_workflows.py` | 4 | FakeLLM, compile + invoke each workflow |
| `test_crm_shared_memory.py` | 3 | YAML bootstrap validation |
| `test_integration_dataops_growth.py` | +2 | CRMOps activation tests added to existing file |

## 7. Not In Scope

- **List sync** (push ad audiences to HubSpot lists) — deferred
- **HubSpot Marketing Hub** (email via HubSpot) — Klaviyo handles email
- **Custom objects** — standard contacts/companies/deals only
- **Bulk operations** — Redshift handles aggregate; HubSpot API is for single-record ops

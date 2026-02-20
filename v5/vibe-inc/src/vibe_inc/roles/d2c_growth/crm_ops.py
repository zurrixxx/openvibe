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

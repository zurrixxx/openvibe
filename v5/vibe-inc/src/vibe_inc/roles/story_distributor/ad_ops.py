"""AdOps operator — manages Meta and Google ad campaigns."""
from openvibe_sdk import Operator, agent_node

from vibe_inc.tools.meta_ads import meta_ads_read, meta_ads_create, meta_ads_update


class AdOps(Operator):
    operator_id = "ad_ops"

    @agent_node(
        tools=[meta_ads_read, meta_ads_create, meta_ads_update],
        output_key="campaign_result",
    )
    def campaign_create(self, state):
        """You are a performance marketing specialist for Vibe hardware products.

        Given a campaign brief, create a complete Meta Ads campaign structure:
        1. Review the brief (product, narrative, audience, budget).
        2. Read the messaging framework from shared memory for the product.
        3. Create a campaign with appropriate objective and naming convention:
           [Product] - [Narrative] - [Audience] - [Date]
        4. Use PAUSED status so human can review before activating.
        5. Always separate Net New audiences from Known (exclude site visitors, video viewers, prior clickers).

        Return a summary of what was created with IDs and configuration."""
        brief = state.get("brief", {})
        return f"Create campaign from brief: {brief}"

    @agent_node(
        tools=[meta_ads_read, meta_ads_update],
        output_key="optimization_result",
    )
    def daily_optimize(self, state):
        """You are a performance marketing optimizer for Vibe hardware products.

        Review all active campaign performance from the last 24 hours:
        1. Read campaign-level and adset-level performance data.
        2. Compare CPA against target benchmarks (Bot: $400, Dot: $300).
        3. Apply these rules:
           - Bid adjustment ≤20%: execute autonomously.
           - Pause any ad with CPA >2x target: execute autonomously.
           - Budget change >$500/day: flag for approval (do not execute).
        4. Always calculate and report Net New CAC separately from Known.
        5. Summarize: what changed, what needs approval, overall health.

        Return a structured optimization report."""
        date = state.get("date", "today")
        return f"Review and optimize all active campaigns for {date}."

    @agent_node(
        tools=[meta_ads_read],
        output_key="report",
    )
    def weekly_report(self, state):
        """You are a performance marketing analyst for Vibe.

        Generate a weekly performance report covering:
        1. Read all campaign data for the past 7 days.
        2. Calculate Net New CAC vs Known CAC by product (Bot, Dot, Board).
        3. Calculate ROAS by channel (Meta, Google).
        4. Report spend efficiency: revenue per visitor, cost per click.
        5. Highlight top 3 performers and bottom 3 underperformers.
        6. Compare against targets: Bot CAC ≤$400, Dot CAC ≤$300, CVR ≥2%.

        Format as progressive disclosure: headline → summary → detailed breakdown."""
        week = state.get("week", "current")
        return f"Generate weekly performance report for {week}."

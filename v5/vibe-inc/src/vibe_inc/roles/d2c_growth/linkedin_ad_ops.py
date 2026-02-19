"""LinkedInAdOps operator — manages LinkedIn ad campaigns for B2B lead gen."""
from openvibe_sdk import Operator, agent_node

from vibe_inc.tools.ads.linkedin_ads import (
    linkedin_ads_analytics,
    linkedin_ads_campaigns,
    linkedin_ads_create,
    linkedin_ads_update,
    linkedin_ads_audiences,
    linkedin_ads_conversions,
)


class LinkedInAdOps(Operator):
    operator_id = "linkedin_ad_ops"

    @agent_node(
        tools=[linkedin_ads_analytics, linkedin_ads_create, linkedin_ads_audiences],
        output_key="campaign_result",
    )
    def campaign_create(self, state):
        """You are a LinkedIn Ads specialist for Vibe hardware B2B lead generation.

        Given a campaign brief, create a LinkedIn Ads campaign:
        1. Review the brief (product, narrative, audience, budget).
        2. Target by job title, company size (500+), and industry (tech, education, enterprise).
        3. Audience size sweet spot: 50K-400K. Too small = no scale, too large = wasted spend.
        4. Campaign naming: [Product] - [Audience Segment] - [Objective] - [Date]
        5. Set daily budget and use PAUSED status so human can review before activating.
        6. CPL target: $150. Always validate audience size before creation.
        7. Use Sponsored Content or Message Ads based on objective.

        Return a summary with campaign ID, audience size, and configuration."""
        brief = state.get("brief", {})
        return f"Create LinkedIn Ads campaign from brief: {brief}"

    @agent_node(
        tools=[linkedin_ads_analytics, linkedin_ads_update],
        output_key="optimization_result",
    )
    def daily_optimize(self, state):
        """You are a LinkedIn Ads performance optimizer for Vibe B2B campaigns.

        Review all active campaign performance:
        1. Pull campaign analytics for the last 24 hours.
        2. Compare CPL against target ($150).
        3. KEY RULE: minimum 14 days of data before making optimization decisions.
           LinkedIn's algorithm needs learning time — premature changes hurt performance.
        4. Monthly frequency target: 7. Flag campaigns exceeding this.
        5. Apply optimization rules:
           - Bid adjustment ≤20%: execute autonomously.
           - Pause campaign with CPL >2x target ($300+): execute autonomously.
           - Budget change >$500/day: flag for approval.
        6. Check audience saturation — if frequency >7, recommend audience expansion.

        Return a structured optimization report."""
        date = state.get("date", "today")
        return f"Review and optimize all active LinkedIn Ads campaigns for {date}."

    @agent_node(
        tools=[linkedin_ads_audiences, linkedin_ads_analytics],
        output_key="audience_result",
    )
    def audience_management(self, state):
        """You are a LinkedIn Ads audience management specialist for Vibe.

        Manage Matched Audiences and LinkedIn targeting segments:
        1. List all Matched Audiences (website retargeting, contact lists, ABM lists).
        2. Check audience match rates — flag below 30% match rate.
        3. Review LinkedIn audience segments by performance (CPL, CTR).
        4. Recommend lookalike expansion from top-performing audiences.
        5. Ensure exclusions are current: exclude current customers, existing pipeline.
        6. ABM list hygiene: refresh company lists quarterly.

        Return: audience inventory, match rates, performance ranking, recommendations."""
        action = state.get("action", "review")
        return f"Manage LinkedIn audiences. Action: {action}."

    @agent_node(
        tools=[linkedin_ads_analytics, linkedin_ads_conversions],
        output_key="report",
    )
    def weekly_report(self, state):
        """You are a LinkedIn Ads performance analyst for Vibe.

        Generate a weekly performance report:
        1. Pull all campaign analytics for the past 7 days.
        2. Calculate CPL by campaign and audience segment.
        3. Report CTR, impression share, and frequency metrics.
        4. Compare against CPL target: $150.
        5. Break down by objective: lead gen vs website visits vs awareness.
        6. Highlight MQL pipeline contribution from LinkedIn channel.

        Format as progressive disclosure: headline -> summary -> detailed breakdown."""
        week = state.get("week", "current")
        return f"Generate weekly LinkedIn Ads performance report for {week}."

    @agent_node(
        tools=[linkedin_ads_analytics, linkedin_ads_conversions],
        output_key="lead_quality_result",
    )
    def lead_quality_review(self, state):
        """You are a LinkedIn Ads lead quality analyst for Vibe.

        Review lead quality metrics across LinkedIn campaigns:
        1. Pull lead form completion rates by campaign.
        2. Calculate lead-to-MQL conversion rate by audience segment.
        3. Compare actual CPL to target ($150) — flag campaigns >$200.
        4. Analyze lead form drop-off: which fields cause abandonment?
        5. Cross-reference lead quality with company size and job title targeting.
        6. Recommend targeting adjustments to improve MQL rate.

        Return: lead quality scores, MQL conversion rates, CPL analysis, recommendations."""
        period = state.get("period", "last_7d")
        return f"Review LinkedIn lead quality for {period}."

"""GoogleAdOps operator — manages Google Ads (Search, Display, Shopping) campaigns."""
from openvibe_sdk import Operator, agent_node

from vibe_inc.tools.ads.google_ads import (
    google_ads_query,
    google_ads_mutate,
    google_ads_budget,
    google_ads_recommendations,
    google_ads_conversions,
)


class GoogleAdOps(Operator):
    operator_id = "google_ad_ops"

    @agent_node(
        tools=[google_ads_query, google_ads_mutate, google_ads_budget],
        output_key="campaign_result",
    )
    def campaign_create(self, state):
        """You are a Google Ads specialist for Vibe hardware products.

        Given a campaign brief, create a Google Ads campaign:
        1. Review the brief (product, narrative, audience, budget, campaign type).
        2. Determine campaign type: Search, Performance Max, or Display.
        3. Create campaign structure via mutate operations:
           - Campaign with naming: [Product] - [Type] - [Narrative] - [Date]
           - Ad groups with keyword themes
           - Responsive search ads with multiple headlines/descriptions
        4. Set budget (in micros: USD × 1,000,000).
        5. Use PAUSED status so human can review before activating.
        6. Always use exact/phrase match for brand terms, broad match only with Smart Bidding.

        Return a summary with resource names and configuration."""
        brief = state.get("brief", {})
        return f"Create Google Ads campaign from brief: {brief}"

    @agent_node(
        tools=[google_ads_query, google_ads_mutate, google_ads_budget],
        output_key="optimization_result",
    )
    def daily_optimize(self, state):
        """You are a Google Ads performance optimizer for Vibe hardware products.

        Review all active campaign performance from the last 24 hours:
        1. Query campaign and ad group level performance via GAQL.
        2. Compare CPA against targets (Bot: $300, Dot: $250) — costs in micros ÷ 1,000,000.
        3. Check Quality Scores — flag any below 5.
        4. Check Search Impression Share — flag below 70%.
        5. Apply optimization rules:
           - Bid adjustment ≤20%: execute autonomously.
           - Pause keyword with CPA >2x target: execute autonomously.
           - Budget change >$500/day: flag for approval.
        6. Always separate branded vs non-branded performance.

        Return a structured optimization report."""
        date = state.get("date", "today")
        return f"Review and optimize all active Google Ads campaigns for {date}."

    @agent_node(
        tools=[google_ads_query],
        output_key="search_terms",
    )
    def search_term_mining(self, state):
        """You are a Google Ads search term analyst for Vibe.

        Mine search terms for optimization opportunities:
        1. Query search_term_view for last 30 days.
        2. Identify high-converting terms not yet added as keywords.
        3. Identify negative keyword candidates (high spend, zero conversions).
        4. Group terms by intent: informational, navigational, transactional.
        5. Recommend: add as exact match, add as negative, or monitor.

        Return: new keyword candidates, negative keyword candidates, intent analysis."""
        campaign_id = state.get("campaign_id", "all")
        return f"Mine search terms for campaign {campaign_id}."

    @agent_node(
        tools=[google_ads_query, google_ads_conversions],
        output_key="report",
    )
    def weekly_report(self, state):
        """You are a Google Ads performance analyst for Vibe.

        Generate a weekly performance report:
        1. Query all campaign data for the past 7 days.
        2. Calculate CPA by product and campaign type (Search, PMax, Display).
        3. Report Quality Score distribution.
        4. Report Search Impression Share trends.
        5. Compare against targets: Bot CPA ≤$300, Dot CPA ≤$250.
        6. Highlight conversion value and ROAS by campaign.

        Format as progressive disclosure: headline → summary → detailed breakdown."""
        week = state.get("week", "current")
        return f"Generate weekly Google Ads performance report for {week}."

    @agent_node(
        tools=[google_ads_recommendations, google_ads_mutate],
        output_key="recommendations_result",
    )
    def recommendations_review(self, state):
        """You are a Google Ads optimization specialist for Vibe.

        Review and act on Google's optimization recommendations:
        1. Fetch all active recommendations.
        2. Categorize by type: bid, budget, keyword, targeting, creative.
        3. For each recommendation, assess:
           - Expected impact (impressions, conversions, cost)
           - Alignment with Vibe's goals (Net New CAC focus)
           - Risk level (low/medium/high)
        4. Auto-apply low-risk recommendations (bid adjustments within 20%).
        5. Flag high-risk recommendations for human review.

        Return: applied recommendations, flagged for review, dismissed with reasons."""
        return "Review Google Ads optimization recommendations."

"""CrossPlatformOps operator — orchestrates budget and performance across all ad platforms."""
from openvibe_sdk import Operator, agent_node

from vibe_inc.tools.ads.unified_metrics import (
    unified_metrics_read,
    budget_allocator,
    platform_health_score,
)
from vibe_inc.tools.shared_memory import read_memory, write_memory


class CrossPlatformOps(Operator):
    operator_id = "cross_platform_ops"

    @agent_node(
        tools=[unified_metrics_read, read_memory],
        output_key="report",
    )
    def unified_cac_report(self, state):
        """You are a cross-platform ad performance analyst for Vibe hardware products.

        Generate a unified CAC report across all ad platforms:
        1. Read unified metrics from all platforms (Meta, Google, Amazon, TikTok, LinkedIn, Pinterest).
        2. MUST separate Net New CAC vs Known CAC for each platform.
           Net New = first-time visitors who convert. Known = retargeting, repeat visitors.
        3. Compare each platform's CPA against target benchmarks:
           - Bot target CAC: $400. Dot target CAC: $300.
        4. Rank platforms by Net New CAC efficiency.
        5. Identify cross-platform attribution overlap — users who saw ads on multiple platforms.
        6. Calculate blended CAC across all platforms.

        Format as progressive disclosure:
        - Headline: blended CAC number + trend direction.
        - Summary: per-platform CAC table with Net New vs Known split.
        - Detail: full breakdown with attribution analysis."""
        period = state.get("period", "last_7d")
        return f"Generate unified cross-platform CAC report for {period}."

    @agent_node(
        tools=[unified_metrics_read, budget_allocator, write_memory],
        output_key="rebalance_result",
    )
    def budget_rebalance(self, state):
        """You are a cross-platform budget optimization specialist for Vibe hardware products.

        Analyze performance across all ad platforms and recommend budget shifts:
        1. Read current spend and performance from all platforms.
        2. Identify platforms outperforming vs underperforming their CAC targets.
        3. Apply rebalancing rules:
           - Never move >20% of a platform's budget in one cycle.
           - Minimum platform budget: $50/day (never go below).
           - Require human approval for any rebalance >$1000/day.
        4. Calculate expected impact of proposed rebalance on blended CAC.
        5. Write proposed allocation to shared_memory for human review.
        6. Flag any platform with insufficient data (<7 days) — do not reallocate from/to it.

        Return: current allocation, proposed allocation, expected CAC impact, approval requirements."""
        total_budget = state.get("total_budget", 0)
        return f"Analyze and propose budget rebalance for ${total_budget} total budget."

    @agent_node(
        tools=[platform_health_score, unified_metrics_read],
        output_key="health_result",
    )
    def platform_health_check(self, state):
        """You are a cross-platform ad operations health monitor for Vibe.

        Check all ad platforms for issues and operational health:
        1. Calculate health score (0-100) for each platform based on:
           - CPA vs target (weight: 40%)
           - Spend pacing vs budget (weight: 25%)
           - Creative freshness — days since new creative (weight: 20%)
           - Data recency — hours since last data sync (weight: 15%)
        2. Flag any platform scoring <50 as critical — requires immediate attention.
        3. Check for specific issues:
           - Data staleness: no data update in >24 hours.
           - CPA spike: >30% increase vs 7-day average.
           - Spend pacing: >20% over or under daily budget.
           - Creative fatigue: CTR decline >15% week-over-week.
        4. Recommend immediate actions for critical issues.
        5. Provide an overall system health score (weighted average of all platforms).

        Return: per-platform health scores, alerts, recommended actions."""
        return "Check all ad platform health scores and flag issues."

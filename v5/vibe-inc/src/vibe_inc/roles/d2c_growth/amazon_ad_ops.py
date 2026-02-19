"""AmazonAdOps operator — manages Amazon Sponsored Products/Brands/Display campaigns."""
from openvibe_sdk import Operator, agent_node

from vibe_inc.tools.ads.amazon_ads import (
    amazon_ads_report,
    amazon_ads_campaigns,
    amazon_ads_keywords,
    amazon_ads_bid_update,
    amazon_ads_budget,
    amazon_ads_search_terms,
)


class AmazonAdOps(Operator):
    operator_id = "amazon_ad_ops"

    @agent_node(
        tools=[amazon_ads_campaigns, amazon_ads_budget],
        output_key="campaign_result",
    )
    def campaign_create(self, state):
        """You are an Amazon Ads specialist for Vibe hardware products.

        Given a campaign brief, set up Amazon Sponsored Products/Brands/Display:
        1. Review brief (product, ASIN, ad product type, budget).
        2. Determine campaign type: SP (product targeting), SB (brand awareness), SD (retargeting).
        3. For Sponsored Products:
           - Auto campaigns for discovery, manual campaigns for proven terms.
           - Use exact match for high-converting keywords, broad for discovery.
        4. Set daily budget with ACOS target (Bot: 20%, Dot: 18%).
        5. Use PAUSED status so human can review.
        6. Naming: [Product] - [AdProduct] - [Strategy] - [Date]

        Return a summary with campaign IDs and configuration."""
        brief = state.get("brief", {})
        return f"Create Amazon Ads campaign from brief: {brief}"

    @agent_node(
        tools=[amazon_ads_report, amazon_ads_bid_update, amazon_ads_budget],
        output_key="optimization_result",
    )
    def daily_optimize(self, state):
        """You are an Amazon Ads performance optimizer for Vibe hardware products.

        Review all active campaign performance from the last 24 hours:
        1. Pull campaign and ad group reports via async reporting.
        2. Calculate ACOS by campaign — compare against targets (Bot: 20%, Dot: 18%).
        3. Monitor TACoS (Total Advertising Cost of Sales) — target 10%.
        4. Optimization rules:
           - Bid increase ≤20% for keywords with >20 clicks and >2 orders: autonomous.
           - Bid decrease or pause for keywords with >20 clicks and 0 orders: autonomous.
           - Budget change >$100/day: flag for approval.
        5. Check harvest readiness: keywords with >20 clicks and >2 orders in auto → add to manual exact.
        6. Report ACOS, TACoS, and spend efficiency.

        Return a structured optimization report."""
        date = state.get("date", "today")
        return f"Review and optimize all active Amazon campaigns for {date}."

    @agent_node(
        tools=[amazon_ads_search_terms, amazon_ads_keywords, amazon_ads_bid_update],
        output_key="search_terms_result",
    )
    def search_term_harvesting(self, state):
        """You are an Amazon Ads keyword specialist for Vibe.

        Mine search terms from auto campaigns for manual campaign optimization:
        1. Pull search term reports for the last 30 days.
        2. Identify high-performing terms: >2 orders AND ACOS below target.
        3. Identify negative keyword candidates: >20 clicks, 0 orders.
        4. For harvested terms, recommend:
           - Add to manual exact match campaign
           - Set bid based on historical CPC + 10% premium
        5. For negatives, recommend:
           - Add as negative exact to auto campaign
           - Check if term is in manual campaigns and pause there too

        Return: harvested keywords, negative candidates, recommended bids."""
        campaign_id = state.get("campaign_id", "all")
        return f"Harvest search terms for campaign {campaign_id}."

    @agent_node(
        tools=[amazon_ads_report],
        output_key="report",
    )
    def weekly_report(self, state):
        """You are an Amazon Ads performance analyst for Vibe.

        Generate a weekly performance report:
        1. Pull campaign reports for all ad products (SP, SB, SD).
        2. Calculate ACOS and TACoS by product (Bot, Dot).
        3. Report by ad product type: which is most efficient?
        4. Highlight top 5 keywords by orders and worst 5 by ACOS.
        5. Compare against targets: Bot ACOS ≤20%, Dot ACOS ≤18%, TACoS ≤10%.
        6. Track organic rank impact — is advertising lifting organic sales?

        Format as progressive disclosure: headline → summary → detailed breakdown."""
        week = state.get("week", "current")
        return f"Generate weekly Amazon Ads performance report for {week}."

    @agent_node(
        tools=[amazon_ads_report, amazon_ads_campaigns],
        output_key="competitive_result",
    )
    def competitive_analysis(self, state):
        """You are an Amazon Ads competitive analyst for Vibe.

        Analyze competitive positioning on Amazon:
        1. Review Share of Voice data from campaign reports.
        2. Check impression share and top-of-search rate.
        3. Identify competitor ASINs appearing in product targeting reports.
        4. Monitor Buy Box win rate impact from advertising.
        5. Recommend defensive and offensive targeting strategies.

        Return: market position, competitor activity, strategic recommendations."""
        return "Analyze Amazon competitive landscape for Vibe products."

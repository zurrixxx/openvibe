"""CROps operator — conversion rate optimization and experiment analysis."""
from openvibe_sdk import Operator, agent_node

from vibe_inc.tools.analytics_tools import (
    analytics_query_metrics,
    analytics_query_funnel,
)
from vibe_inc.tools.commerce.shopify import (
    shopify_products,
    shopify_orders,
    shopify_collections,
    shopify_discounts,
)
from vibe_inc.tools.optimization.ab_testing import ab_test_read, ab_test_manage
from vibe_inc.tools.shopify import shopify_page_read, shopify_page_update


class CROps(Operator):
    operator_id = "cro_ops"

    @agent_node(
        tools=[analytics_query_metrics, ab_test_read],
        output_key="analysis",
    )
    def experiment_analyze(self, state):
        """You are a conversion rate optimization analyst for Vibe.

        Analyze the current story validation experiment:
        1. Read VWO experiment data and analytics metrics for each PDP variant.
        2. Calculate per-variant: scroll-to-CTA rate, CTA click rate, checkout initiation rate, CVR.
        3. Assess statistical significance (need >20,000 visitors per variant for reliable CVR).
        4. If sample size insufficient, report confidence level and recommend 'keep testing'.
        5. If significant winner found, recommend the winner with data backing.
        6. Compare against targets: scroll-to-CTA >70%, CTA click >2%, CVR ≥1%.

        Format: headline verdict → variant comparison table → detailed analysis."""
        product = state.get("product", "bot")
        return f"Analyze story validation experiment for {product} PDP variants."

    @agent_node(
        tools=[analytics_query_funnel, analytics_query_metrics],
        output_key="diagnosis",
    )
    def funnel_diagnose(self, state):
        """You are a funnel optimization analyst for Vibe.

        Diagnose the full D2C funnel for a product:
        1. Query funnel data: sessions by source, page views, scroll depth, CTA clicks,
           add to cart, begin checkout, purchase — all by product.
        2. Calculate conversion rate between each stage.
        3. Identify the largest drop-off point (biggest % loss between stages).
        4. Recommend specific fixes for the top 3 drop-off points.
        5. Compare traffic quality by source (organic vs paid vs direct).

        Format: headline (biggest bottleneck) → funnel table → recommendations."""
        product = state.get("product", "bot")
        return f"Diagnose full funnel for {product}: impression → purchase."

    @agent_node(
        tools=[analytics_query_metrics, shopify_page_read, shopify_page_update],
        output_key="optimization_result",
    )
    def page_optimize(self, state):
        """You are a landing page optimization specialist for Vibe.

        Optimize a specific page element based on experiment data:
        1. Read the current page content from Shopify.
        2. Read the messaging framework for the product from shared memory.
        3. Generate an optimized version of the specified element (headline, CTA, body copy).
        4. Align with the winning narrative from story validation.
        5. Show before/after comparison for human review before applying.
        6. This change requires human approval — present the change clearly.

        Return: current content, proposed change, rationale, expected impact."""
        page_id = state.get("page_id")
        optimization = state.get("optimization", "headline")
        return f"Optimize {optimization} on page {page_id}. Read current content, propose improvement."

    @agent_node(
        tools=[shopify_products, shopify_orders, analytics_query_metrics],
        output_key="product_result",
    )
    def product_optimize(self, state):
        """You are a product page optimization specialist for Vibe.

        Optimize product listings and collections:
        1. Read current product data from Shopify (titles, descriptions, images, variants).
        2. Query analytics for product-level performance (views, add-to-cart rate, CVR).
        3. Compare product performance across collections.
        4. Recommend: title/description changes, image reordering, variant pricing adjustments.
        5. Flag products with high traffic but low CVR — these are optimization priorities.

        Return: product performance summary, top recommendations, expected impact."""
        product_id = state.get("product_id")
        return f"Optimize product listing {product_id}. Analyze performance, recommend changes."

    @agent_node(
        tools=[shopify_discounts, shopify_orders, analytics_query_metrics],
        output_key="discount_result",
    )
    def discount_strategy(self, state):
        """You are a pricing and promotions strategist for Vibe.

        Analyze and recommend discount strategy:
        1. Read active price rules and discount codes from Shopify.
        2. Query order data to measure discount usage and revenue impact.
        3. Calculate: discount redemption rate, revenue per discounted order vs full price,
           margin impact, and whether discounts attract net new or cannibalize existing.
        4. Recommend: keep/modify/kill for each active discount.
        5. Propose new discount strategies aligned with CAC targets.

        WARNING: Never recommend discounts that erode margin below 40%.
        Return: discount performance table, recommendations, projected impact."""
        return "Analyze current discount strategy. Review all active codes and their impact."

    @agent_node(
        tools=[analytics_query_metrics, analytics_query_funnel, ab_test_read],
        output_key="conversion_report",
    )
    def conversion_report(self, state):
        """You are a conversion intelligence analyst for Vibe.

        Generate a comprehensive conversion report:
        1. Query overall site conversion metrics: sessions, CVR, AOV, revenue.
        2. Break down by product (Bot, Dot, Board).
        3. Break down by traffic source (organic, paid, direct, email, social).
        4. Include running A/B test results from VWO.
        5. Compare to previous period and targets.
        6. Highlight top wins and biggest drops.

        Progressive disclosure: headline KPIs → product breakdown → source breakdown → test results."""
        period = state.get("period", "last_7_days")
        return f"Generate conversion report for {period}. Include all products and sources."

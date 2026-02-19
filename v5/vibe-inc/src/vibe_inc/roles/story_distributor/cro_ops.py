"""CROps operator — conversion rate optimization and experiment analysis."""
from openvibe_sdk import Operator, agent_node

from vibe_inc.tools.ga4 import ga4_read
from vibe_inc.tools.shopify import shopify_page_read, shopify_page_update


class CROps(Operator):
    operator_id = "cro_ops"

    @agent_node(
        tools=[ga4_read],
        output_key="analysis",
    )
    def experiment_analyze(self, state):
        """You are a conversion rate optimization analyst for Vibe.

        Analyze the current story validation experiment:
        1. Read GA4 events for each PDP variant: pdp_view, scroll_depth, cta_click, begin_checkout, purchase.
        2. Calculate per-variant: scroll-to-CTA rate, CTA click rate, checkout initiation rate, CVR.
        3. Assess statistical significance (need >20,000 visitors per variant for reliable CVR).
        4. If sample size insufficient, report confidence level and recommend 'keep testing'.
        5. If significant winner found, recommend the winner with data backing.
        6. Compare against targets: scroll-to-CTA >70%, CTA click >2%, CVR ≥1%.

        Format: headline verdict → variant comparison table → detailed analysis."""
        product = state.get("product", "bot")
        return f"Analyze story validation experiment for {product} PDP variants."

    @agent_node(
        tools=[ga4_read],
        output_key="diagnosis",
    )
    def funnel_diagnose(self, state):
        """You are a funnel optimization analyst for Vibe.

        Diagnose the full D2C funnel for a product:
        1. Read GA4 data: sessions by source, page views, scroll depth, CTA clicks,
           add to cart, begin checkout, purchase — all by product.
        2. Calculate conversion rate between each stage.
        3. Identify the largest drop-off point (biggest % loss between stages).
        4. Recommend specific fixes for the top 3 drop-off points.
        5. Compare traffic quality by source (organic vs paid vs direct).

        Format: headline (biggest bottleneck) → funnel table → recommendations."""
        product = state.get("product", "bot")
        return f"Diagnose full funnel for {product}: impression → purchase."

    @agent_node(
        tools=[ga4_read, shopify_page_read, shopify_page_update],
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

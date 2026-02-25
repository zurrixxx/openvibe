"""DailyReportOps operator — daily growth report from Redshift data."""

import json

from openvibe_sdk import Operator, agent_node

from vibe_inc.tools.shared_memory import read_memory

from .daily_report_queries import fetch_l1, fetch_l2, fetch_l3


class DailyReportOps(Operator):
    operator_id = "daily_report_ops"

    def fetch_data(self, state):
        """Deterministic data fetching — runs pre-written SQL against Redshift."""
        date = state.get("date")
        return {
            "l1_data": fetch_l1(date),
            "l2_data": fetch_l2(date),
            "l3_data": fetch_l3(date),
        }

    @agent_node(
        tools=[read_memory],
        output_key="report",
    )
    def interpret(self, state):
        """You are a D2C growth analyst for Vibe hardware products (Board, Bot, Dot).

        You receive three layers of pre-queried Redshift data:
        - L1: business outcomes (revenue, orders, CAC by product)
        - L2: channel efficiency (per-platform spend, CPA, trends)
        - L3: funnel signal (traffic, conversion rates, drop-offs)

        Produce a Daily Growth Report in this exact structure:

        1. HEADLINE — one sentence: single most important thing today.
           Flag: 🔴 (action needed), ⚠️ (watch), ✅ (all clear).
           Red if: any L1 metric >20% off target OR any platform CPA >1.5x target.
           Yellow if: any L1 metric >10% off OR trending wrong 3+ days.
           Green if: all within targets and stable.

        2. L1 TABLE — revenue + CAC by product, columns: Yesterday | 7d Avg | 28d Avg | Target.

        3. L2 TABLE — per-platform: Spend | CPA | vs Target | vs 7d Avg | Flag.
           Include Amazon ACOS separately.
           List top campaigns by worst CPA for actionability.

        4. L3 TABLE — traffic by channel and funnel steps with conversion rates vs 7d avg.

        5. RECOMMENDED ACTIONS — numbered, specific, with expected impact.
           Format: [PLATFORM] verb + specific target + reason + expected impact.

        Rules:
        - Net New CAC is the only CAC that matters. If the data does not separate
          Net New vs Known, flag this as a measurement gap in the headline.
        - Never say "optimize" without saying what specifically to do.
        - Classify anomalies: structural (trend 3+ days) vs noise (single day).
        - If data is missing or empty, say so. Do not fabricate numbers.
        - Benchmarks: Bot CAC ≤$400, Dot CAC ≤$300, Board ACOS ≤20%.
        - Use read_memory("performance/cac-benchmarks") and
          read_memory("performance/platform_benchmarks") for exact thresholds.
        - Every number must have context: vs target, vs 7d avg, or vs 28d avg."""
        l1 = json.dumps(state.get("l1_data", {}), indent=2, default=str)
        l2 = json.dumps(state.get("l2_data", {}), indent=2, default=str)
        l3 = json.dumps(state.get("l3_data", {}), indent=2, default=str)
        date = state.get("date", "yesterday")
        return (
            f"Generate the Daily Growth Report for {date}.\n\n"
            f"L1 (Business Outcomes):\n{l1}\n\n"
            f"L2 (Channel Efficiency):\n{l2}\n\n"
            f"L3 (Funnel Signal):\n{l3}"
        )

#!/usr/bin/env python3
"""Smoke test: all 20 non-HubSpot workflows via LangGraph → Claude API.

Skipped (require HubSpot API key):
  - revenue_ops / new_lead      (lead_qualification)
  - revenue_ops / weekday_deals (deal_support)

Usage:
    python smoke_all.py           # run all 20 workflows
    python smoke_all.py --fast    # run 1 per operator (5 total)
"""

from __future__ import annotations

import os
import sys
import time
from typing import Any

from dotenv import load_dotenv

load_dotenv()

# Suppress LangFuse noise
os.environ.setdefault("LANGFUSE_PUBLIC_KEY", "")

TESTS: list[dict[str, Any]] = [
    # ── Company Intel ──────────────────────────────────────────────
    {
        "op": "company_intel",
        "trigger": "query",
        "label": "company_intel / research",
        "input": {"company_name": "Anthropic"},
        "check": "report",
    },
    # ── Revenue Ops (skip new_lead + weekday_deals — HubSpot) ─────
    {
        "op": "revenue_ops",
        "trigger": "lead_qualified",
        "label": "revenue_ops / engagement",
        "input": {
            "buyer_profile": {
                "name": "Sarah Chen",
                "title": "VP Operations",
                "company": "Acme Corp",
                "industry": "Manufacturing",
            },
            "segment": "Mid-Market",
            "contact_id": "test-001",
        },
        "check": "final_plan",
    },
    {
        "op": "revenue_ops",
        "trigger": "lead_nurture",
        "label": "revenue_ops / nurture_sequence",
        "input": {
            "lead_data": {
                "name": "Bob Torres",
                "company": "TechCorp",
                "email": "bob@techcorp.com",
            },
            "lead_score": 55,
            "touches_completed": 0,
            "max_touches": 4,
            "touch_interval_days": 3,
        },
        "check": "route",
    },
    {
        "op": "revenue_ops",
        "trigger": "daily_intel",
        "label": "revenue_ops / buyer_intelligence",
        "input": {},
        "check": "brief",
    },
    # ── Content Engine ─────────────────────────────────────────────
    {
        "op": "content_engine",
        "trigger": "weekly_research",
        "label": "content_engine / segment_research",
        "input": {
            "segment_data": [
                {"name": "SMB", "size": 5000, "characteristics": ["cost-sensitive", "fast decisions"]},
                {"name": "Mid-Market", "size": 1200, "characteristics": ["needs ROI proof", "multi-stakeholder"]},
            ]
        },
        "check": "segment_report",
    },
    {
        "op": "content_engine",
        "trigger": "message_testing",
        "label": "content_engine / message_testing",
        "input": {
            "topic": "AI adoption for B2B sales teams",
            "segment_data": [{"name": "VP Sales", "size": 800, "characteristics": ["quota-driven"]}],
        },
        "check": "recommendation",
    },
    {
        "op": "content_engine",
        "trigger": "daily_content",
        "label": "content_engine / content_generation",
        "input": {
            "topic": "How AI collaboration tools boost remote team productivity",
        },
        "check": "polished_content",
    },
    {
        "op": "content_engine",
        "trigger": "content_ready",
        "label": "content_engine / repurposing",
        "input": {
            "source_content": (
                "AI collaboration tools are transforming how distributed teams work. "
                "Teams using AI assistants report 40% faster decision-making and "
                "significantly improved async communication quality."
            ),
            "content_formats": ["social_post", "email_snippet", "blog_summary"],
        },
        "check": "adapted_content",
    },
    {
        "op": "content_engine",
        "trigger": "repurposed_ready",
        "label": "content_engine / distribution",
        "input": {
            "adapted_content": {
                "social_post": "AI tools are changing how teams work. 40% faster decisions.",
                "email_snippet": "See how AI collaboration boosts your team's output.",
            },
        },
        "check": "distribution_report",
    },
    {
        "op": "content_engine",
        "trigger": "weekly_optimization",
        "label": "content_engine / journey_optimization",
        "input": {
            "funnel_metrics": {
                "visitors": 12000,
                "leads": 480,
                "mql": 144,
                "sql": 43,
                "closed": 11,
            }
        },
        "check": "optimization_recommendations",
    },
    # ── Customer Success ───────────────────────────────────────────
    {
        "op": "customer_success",
        "trigger": "deal_won",
        "label": "customer_success / onboarding",
        "input": {
            "customer_name": "Acme Corp",
            "customer_id": "c-001",
        },
        "check": "milestones",
    },
    {
        "op": "customer_success",
        "trigger": "weekly_advisory",
        "label": "customer_success / success_advisory",
        "input": {
            "accounts": [
                {"name": "TechCo", "health": 72, "mrr": 5000, "days_since_login": 3},
                {"name": "BuildCo", "health": 45, "mrr": 12000, "days_since_login": 14},
            ]
        },
        "check": "playbooks",
    },
    {
        "op": "customer_success",
        "trigger": "daily_health",
        "label": "customer_success / health_monitoring",
        "input": {},
        "check": "health_score",
    },
    {
        "op": "customer_success",
        "trigger": "weekly_expansion",
        "label": "customer_success / expansion_scan",
        "input": {
            "usage_data": {
                "accounts": [
                    {"name": "GrowCo", "seats_used": 8, "seats_licensed": 10, "features_used": ["boards", "meetings"]},
                    {"name": "ScaleCo", "seats_used": 25, "seats_licensed": 25, "features_used": ["boards"]},
                ]
            }
        },
        "check": "opportunities",
    },
    {
        "op": "customer_success",
        "trigger": "weekly_voice",
        "label": "customer_success / customer_voice",
        "input": {
            "feedback": [
                {"source": "intercom", "text": "Wish the board export was faster", "sentiment": "neutral"},
                {"source": "nps", "text": "Love the meeting integration", "sentiment": "positive"},
                {"source": "support", "text": "Can't find the template library", "sentiment": "negative"},
            ]
        },
        "check": "voice_report",
    },
    {
        "op": "customer_success",
        "trigger": "revenue_escalation",
        "label": "customer_success / urgent_review",
        "input": {
            "customer_name": "BigCo",
            "deal_id": "d-042",
            "reason": "Payment 30 days overdue, usage dropped 60% in last 2 weeks",
        },
        "check": "recommendation",
    },
    # ── Market Intel ──────────────────────────────────────────────
    {
        "op": "market_intel",
        "trigger": "daily_funnel",
        "label": "market_intel / funnel_monitor",
        "input": {
            "funnel_metrics": {
                "visitors": 9800,
                "leads": 392,
                "mql": 117,
                "sql": 35,
                "closed_won": 8,
                "prev_week": {"visitors": 10200, "leads": 460, "mql": 138},
            }
        },
        "check": "funnel_brief",
    },
    {
        "op": "market_intel",
        "trigger": "weekday_forecast",
        "label": "market_intel / deal_risk_forecast",
        "input": {
            "deals": [
                {"id": "d-101", "name": "Acme", "value": 24000, "stage": "proposal", "days_in_stage": 12, "close_date": "2026-03-15"},
                {"id": "d-102", "name": "BigCo", "value": 60000, "stage": "negotiation", "days_in_stage": 28, "close_date": "2026-02-28"},
            ]
        },
        "check": "forecast_report",
    },
    {
        "op": "market_intel",
        "trigger": "weekly_conversations",
        "label": "market_intel / conversation_analysis",
        "input": {
            "transcripts": [
                {"id": "t-001", "prospect": "Acme", "outcome": "demo booked", "text": "They asked a lot about integrations with Slack and HubSpot."},
                {"id": "t-002", "prospect": "TechCo", "outcome": "lost", "text": "Price was the main objection. They went with a cheaper option."},
            ]
        },
        "check": "conversation_summary",
    },
    {
        "op": "market_intel",
        "trigger": "query",
        "label": "market_intel / nl_query",
        "input": {"question": "Which deals are most at risk of slipping this quarter?"},
        "check": "answer",
    },
]

FAST_TESTS = [t for t in TESTS if t["op"] in {
    "company_intel", "revenue_ops", "content_engine", "customer_success", "market_intel"
} and TESTS.index(t) in {0, 1, 4, 10, 16}]


def run_tests(tests: list[dict]) -> None:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set")
        sys.exit(1)

    from vibe_ai_ops.main import build_system
    print("Building operator system...")
    system = build_system()
    runtime = system["runtime"]
    print(f"  {system['operator_count']} operators, {system['summary']['workflows']} workflows loaded\n")

    passed = 0
    failed = 0
    errors: list[tuple[str, str]] = []

    print(f"Running {len(tests)} workflow smoke tests...\n")
    print(f"{'Workflow':<45} {'Result':<10} {'Time':>6}  Output key")
    print("-" * 80)

    for t in tests:
        label = t["label"]
        start = time.time()
        try:
            result = runtime.activate(t["op"], t["trigger"], t["input"])
            duration = time.time() - start
            check_key = t["check"]
            value = result.get(check_key) if isinstance(result, dict) else None
            has_output = bool(value)
            status = "PASS" if has_output else "WARN"
            if has_output:
                passed += 1
                preview = str(value)[:60].replace("\n", " ")
                print(f"  {label:<43} {status:<10} {duration:>5.1f}s  {check_key}={preview!r}")
            else:
                failed += 1
                print(f"  {label:<43} {status:<10} {duration:>5.1f}s  '{check_key}' key missing/empty")
                errors.append((label, f"'{check_key}' key not found in result"))
        except Exception as e:
            duration = time.time() - start
            failed += 1
            short_err = str(e)[:80]
            print(f"  {label:<43} {'FAIL':<10} {duration:>5.1f}s  {short_err}")
            errors.append((label, str(e)))

    print("\n" + "=" * 80)
    print(f"  Results: {passed} passed, {failed} failed / {len(tests)} total")
    if errors:
        print("\n  Failures:")
        for name, err in errors:
            print(f"    - {name}: {err[:100]}")
    print("=" * 80)

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    fast = "--fast" in sys.argv
    run_tests(FAST_TESTS if fast else TESTS)

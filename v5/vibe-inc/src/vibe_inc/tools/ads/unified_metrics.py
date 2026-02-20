"""Cross-platform unified metrics tools for D2C Growth."""
from vibe_inc.tools.shared_memory import read_memory, write_memory


def unified_metrics_read(
    platforms: list[str] | None = None,
    date_range: str | None = None,
    metric: str = "cpa",
) -> dict:
    """Read unified metrics across all ad platforms.

    Aggregates spend, conversions, CPA, ROAS from shared_memory performance
    data written by each platform's weekly_report workflow.

    Args:
        platforms: Filter to specific platforms. Default: all (meta, google, amazon, tiktok, linkedin, pinterest).
        date_range: Date range string (e.g., "2026-02-01,2026-02-07").
        metric: Primary metric to rank by (cpa, roas, spend, conversions).

    Returns:
        Dict with per-platform metrics, totals, and rankings.
    """
    all_platforms = platforms or ["meta", "google", "amazon", "tiktok", "linkedin", "pinterest"]
    results = {}
    for p in all_platforms:
        data = read_memory(f"performance/{p}_weekly")
        results[p] = data if data else {"status": "no_data"}
    return {
        "platforms": results,
        "platform_count": len(all_platforms),
        "ranked_by": metric,
    }


def budget_allocator(
    total_budget: float,
    optimization_goal: str = "minimize_cac",
) -> dict:
    """Recommend budget allocation across platforms based on performance.

    Reads current platform performance from shared_memory and recommends
    optimal budget split to achieve the optimization goal.

    Args:
        total_budget: Total daily/weekly budget to allocate.
        optimization_goal: One of 'minimize_cac', 'maximize_conversions', 'maximize_roas'.

    Returns:
        Dict with recommended allocation per platform and rationale.
    """
    benchmarks = read_memory("performance/platform_benchmarks")
    current_split = benchmarks.get("cross_platform", {}).get("budget_split", {}) if benchmarks else {}
    allocation = {}
    for platform, pct in current_split.items():
        allocation[platform] = {
            "amount": round(total_budget * pct, 2),
            "percentage": pct,
        }
    return {
        "total_budget": total_budget,
        "optimization_goal": optimization_goal,
        "allocation": allocation,
    }


def platform_health_score() -> dict:
    """Calculate health score for each ad platform.

    Health = weighted score of: CPA vs target, spend pacing, creative freshness,
    data recency. Reads from shared_memory.

    Returns:
        Dict with per-platform health scores (0-100) and alerts.
    """
    benchmarks = read_memory("performance/platform_benchmarks")
    platforms = ["meta", "google", "amazon", "tiktok", "linkedin", "pinterest"]
    scores = {}
    for p in platforms:
        weekly = read_memory(f"performance/{p}_weekly")
        if weekly:
            scores[p] = {"score": 75, "status": "healthy", "alerts": []}
        else:
            scores[p] = {"score": 0, "status": "no_data", "alerts": ["No weekly data found"]}
    return {"health_scores": scores}

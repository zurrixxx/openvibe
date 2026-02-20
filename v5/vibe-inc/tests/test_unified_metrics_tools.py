from unittest.mock import patch


def test_unified_metrics_read_returns_platforms():
    from vibe_inc.tools.ads.unified_metrics import unified_metrics_read

    with patch("vibe_inc.tools.ads.unified_metrics.read_memory", return_value={"spend": 1000, "conversions": 50}):
        result = unified_metrics_read()

    assert "platforms" in result
    assert result["platform_count"] == 6


def test_unified_metrics_read_filters_platforms():
    from vibe_inc.tools.ads.unified_metrics import unified_metrics_read

    with patch("vibe_inc.tools.ads.unified_metrics.read_memory", return_value={"spend": 500}):
        result = unified_metrics_read(platforms=["meta", "google"])

    assert result["platform_count"] == 2


def test_unified_metrics_read_has_docstring():
    from vibe_inc.tools.ads.unified_metrics import unified_metrics_read
    assert unified_metrics_read.__doc__ is not None


def test_budget_allocator_returns_allocation():
    from vibe_inc.tools.ads.unified_metrics import budget_allocator

    mock_benchmarks = {"cross_platform": {"budget_split": {"google": 0.37, "meta": 0.28, "amazon": 0.15, "tiktok": 0.10, "linkedin": 0.05, "pinterest": 0.05}}}
    with patch("vibe_inc.tools.ads.unified_metrics.read_memory", return_value=mock_benchmarks):
        result = budget_allocator(total_budget=10000.0)

    assert result["total_budget"] == 10000.0
    assert "allocation" in result
    assert result["allocation"]["google"]["amount"] == 3700.0


def test_platform_health_score_returns_scores():
    from vibe_inc.tools.ads.unified_metrics import platform_health_score

    with patch("vibe_inc.tools.ads.unified_metrics.read_memory", return_value={"spend": 100}):
        result = platform_health_score()

    assert "health_scores" in result
    assert "meta" in result["health_scores"]

"""LangGraph workflow factories for CrossPlatformOps."""
from typing import TypedDict

from langgraph.graph import StateGraph


class UnifiedReportState(TypedDict, total=False):
    period: str
    report: str


class RebalanceState(TypedDict, total=False):
    total_budget: float
    rebalance_result: str


class HealthCheckState(TypedDict, total=False):
    health_result: str


def create_unified_cac_report_graph(operator):
    """Unified CAC report: aggregate all platforms → Net New vs Known → rank."""
    graph = StateGraph(UnifiedReportState)
    graph.add_node("report", operator.unified_cac_report)
    graph.set_entry_point("report")
    graph.set_finish_point("report")
    return graph.compile()


def create_budget_rebalance_graph(operator):
    """Budget rebalance: read performance → propose shifts → write for approval."""
    graph = StateGraph(RebalanceState)
    graph.add_node("rebalance", operator.budget_rebalance)
    graph.set_entry_point("rebalance")
    graph.set_finish_point("rebalance")
    return graph.compile()


def create_platform_health_check_graph(operator):
    """Platform health check: score all platforms → flag critical → recommend actions."""
    graph = StateGraph(HealthCheckState)
    graph.add_node("check", operator.platform_health_check)
    graph.set_entry_point("check")
    graph.set_finish_point("check")
    return graph.compile()

"""LangGraph workflow factories for EmailOps."""
from typing import TypedDict

from langgraph.graph import StateGraph


class EmailCampaignState(TypedDict, total=False):
    brief: dict
    campaign_result: str


class FlowOptimizeState(TypedDict, total=False):
    flow_id: str
    flow_result: str


class SegmentRefreshState(TypedDict, total=False):
    segment_result: str


class EmailReportState(TypedDict, total=False):
    period: str
    report: str


def create_email_campaign_create_graph(operator):
    """Email campaign creation: segment targeting + A/B subject lines."""
    graph = StateGraph(EmailCampaignState)
    graph.add_node("create", operator.campaign_create)
    graph.set_entry_point("create")
    graph.set_finish_point("create")
    return graph.compile()


def create_email_flow_optimize_graph(operator):
    """Email flow optimization: review flows + timing + branching."""
    graph = StateGraph(FlowOptimizeState)
    graph.add_node("optimize", operator.flow_optimize)
    graph.set_entry_point("optimize")
    graph.set_finish_point("optimize")
    return graph.compile()


def create_email_segment_refresh_graph(operator):
    """Email segment refresh: overlap + staleness + engagement decay."""
    graph = StateGraph(SegmentRefreshState)
    graph.add_node("refresh", operator.segment_refresh)
    graph.set_entry_point("refresh")
    graph.set_finish_point("refresh")
    return graph.compile()


def create_email_lifecycle_report_graph(operator):
    """Email lifecycle report: open rate + click rate + RPE + list growth."""
    graph = StateGraph(EmailReportState)
    graph.add_node("report", operator.lifecycle_report)
    graph.set_entry_point("report")
    graph.set_finish_point("report")
    return graph.compile()

"""LangGraph workflow factories for D2C Growth."""
from typing import TypedDict

from langgraph.graph import StateGraph


class OptimizeState(TypedDict, total=False):
    date: str
    optimization_result: str


class CampaignState(TypedDict, total=False):
    brief: dict
    campaign_result: str


class ExperimentState(TypedDict, total=False):
    product: str
    analysis: str


class FunnelState(TypedDict, total=False):
    product: str
    diagnosis: str


class PageOptimizeState(TypedDict, total=False):
    page_id: str
    optimization: str
    rationale: str
    optimization_result: str


class ReportState(TypedDict, total=False):
    week: str
    report: str


class AudienceRefreshState(TypedDict, total=False):
    action: str
    audience_result: str


# --- MetaAdOps workflows ---


def create_meta_daily_optimize_graph(operator):
    """Meta daily optimization: read performance → analyze → adjust bids."""
    graph = StateGraph(OptimizeState)
    graph.add_node("optimize", operator.daily_optimize)
    graph.set_entry_point("optimize")
    graph.set_finish_point("optimize")
    return graph.compile()


def create_meta_campaign_create_graph(operator):
    """Meta campaign creation: read brief → build campaign → return IDs."""
    graph = StateGraph(CampaignState)
    graph.add_node("create", operator.campaign_create)
    graph.set_entry_point("create")
    graph.set_finish_point("create")
    return graph.compile()


def create_meta_audience_refresh_graph(operator):
    """Meta audience refresh: review audiences → flag stale → recommend."""
    graph = StateGraph(AudienceRefreshState)
    graph.add_node("refresh", operator.audience_refresh)
    graph.set_entry_point("refresh")
    graph.set_finish_point("refresh")
    return graph.compile()


def create_experiment_analyze_graph(operator):
    """Experiment analysis: read GA4 events → compute significance → recommend."""
    graph = StateGraph(ExperimentState)
    graph.add_node("analyze", operator.experiment_analyze)
    graph.set_entry_point("analyze")
    graph.set_finish_point("analyze")
    return graph.compile()


def create_funnel_diagnose_graph(operator):
    """Funnel diagnosis: read full funnel → identify drop-offs → recommend fixes."""
    graph = StateGraph(FunnelState)
    graph.add_node("diagnose", operator.funnel_diagnose)
    graph.set_entry_point("diagnose")
    graph.set_finish_point("diagnose")
    return graph.compile()


def create_page_optimize_graph(operator):
    """Page optimization: read page → propose change → apply (with approval)."""
    graph = StateGraph(PageOptimizeState)
    graph.add_node("optimize", operator.page_optimize)
    graph.set_entry_point("optimize")
    graph.set_finish_point("optimize")
    return graph.compile()


def create_meta_weekly_report_graph(operator):
    """Meta weekly report: read all data → generate Net New vs Known report."""
    graph = StateGraph(ReportState)
    graph.add_node("report", operator.weekly_report)
    graph.set_entry_point("report")
    graph.set_finish_point("report")
    return graph.compile()


# --- GoogleAdOps workflows ---


class SearchTermState(TypedDict, total=False):
    campaign_id: str
    search_terms: str


class RecommendationsState(TypedDict, total=False):
    recommendations_result: str


def create_google_daily_optimize_graph(operator):
    """Google daily optimization: query performance → analyze → adjust bids."""
    graph = StateGraph(OptimizeState)
    graph.add_node("optimize", operator.daily_optimize)
    graph.set_entry_point("optimize")
    graph.set_finish_point("optimize")
    return graph.compile()


def create_google_campaign_create_graph(operator):
    """Google campaign creation: read brief → build campaign → return resource names."""
    graph = StateGraph(CampaignState)
    graph.add_node("create", operator.campaign_create)
    graph.set_entry_point("create")
    graph.set_finish_point("create")
    return graph.compile()


def create_google_search_term_mining_graph(operator):
    """Google search term mining: query terms → categorize → recommend."""
    graph = StateGraph(SearchTermState)
    graph.add_node("mine", operator.search_term_mining)
    graph.set_entry_point("mine")
    graph.set_finish_point("mine")
    return graph.compile()


def create_google_weekly_report_graph(operator):
    """Google weekly report: query metrics → analyze → format report."""
    graph = StateGraph(ReportState)
    graph.add_node("report", operator.weekly_report)
    graph.set_entry_point("report")
    graph.set_finish_point("report")
    return graph.compile()


def create_google_recommendations_review_graph(operator):
    """Google recommendations review: fetch → categorize → apply/flag."""
    graph = StateGraph(RecommendationsState)
    graph.add_node("review", operator.recommendations_review)
    graph.set_entry_point("review")
    graph.set_finish_point("review")
    return graph.compile()

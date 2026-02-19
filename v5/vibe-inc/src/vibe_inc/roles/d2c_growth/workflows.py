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


# --- AmazonAdOps workflows ---


class SearchTermHarvestState(TypedDict, total=False):
    campaign_id: str
    search_terms_result: str


class CompetitiveState(TypedDict, total=False):
    competitive_result: str


def create_amazon_daily_optimize_graph(operator):
    """Amazon daily optimization: pull reports → check ACOS → adjust bids."""
    graph = StateGraph(OptimizeState)
    graph.add_node("optimize", operator.daily_optimize)
    graph.set_entry_point("optimize")
    graph.set_finish_point("optimize")
    return graph.compile()


def create_amazon_campaign_create_graph(operator):
    """Amazon campaign creation: read brief → set up SP/SB/SD campaign."""
    graph = StateGraph(CampaignState)
    graph.add_node("create", operator.campaign_create)
    graph.set_entry_point("create")
    graph.set_finish_point("create")
    return graph.compile()


def create_amazon_search_term_harvest_graph(operator):
    """Amazon search term harvesting: mine auto → add to manual exact."""
    graph = StateGraph(SearchTermHarvestState)
    graph.add_node("harvest", operator.search_term_harvesting)
    graph.set_entry_point("harvest")
    graph.set_finish_point("harvest")
    return graph.compile()


def create_amazon_weekly_report_graph(operator):
    """Amazon weekly report: pull all ad product data → analyze ACOS/TACoS."""
    graph = StateGraph(ReportState)
    graph.add_node("report", operator.weekly_report)
    graph.set_entry_point("report")
    graph.set_finish_point("report")
    return graph.compile()


def create_amazon_competitive_analysis_graph(operator):
    """Amazon competitive analysis: SOV, impression share, competitor ASINs."""
    graph = StateGraph(CompetitiveState)
    graph.add_node("analyze", operator.competitive_analysis)
    graph.set_entry_point("analyze")
    graph.set_finish_point("analyze")
    return graph.compile()


# --- TikTokAdOps workflows ---


class CreativeRefreshState(TypedDict, total=False):
    creative_result: str


def create_tiktok_daily_optimize_graph(operator):
    """TikTok daily optimization: check learning phase → adjust bids."""
    graph = StateGraph(OptimizeState)
    graph.add_node("optimize", operator.daily_optimize)
    graph.set_entry_point("optimize")
    graph.set_finish_point("optimize")
    return graph.compile()


def create_tiktok_campaign_create_graph(operator):
    """TikTok campaign creation: read brief → set budget for learning phase."""
    graph = StateGraph(CampaignState)
    graph.add_node("create", operator.campaign_create)
    graph.set_entry_point("create")
    graph.set_finish_point("create")
    return graph.compile()


def create_tiktok_creative_refresh_graph(operator):
    """TikTok creative refresh: detect fatigue → recommend replacements."""
    graph = StateGraph(CreativeRefreshState)
    graph.add_node("refresh", operator.creative_refresh)
    graph.set_entry_point("refresh")
    graph.set_finish_point("refresh")
    return graph.compile()


def create_tiktok_weekly_report_graph(operator):
    """TikTok weekly report: pull metrics → analyze CPA → format."""
    graph = StateGraph(ReportState)
    graph.add_node("report", operator.weekly_report)
    graph.set_entry_point("report")
    graph.set_finish_point("report")
    return graph.compile()


# --- LinkedInAdOps workflows ---


class LeadQualityState(TypedDict, total=False):
    lead_quality_result: str


def create_linkedin_daily_optimize_graph(operator):
    """LinkedIn daily optimization: check 14-day data minimum → adjust."""
    graph = StateGraph(OptimizeState)
    graph.add_node("optimize", operator.daily_optimize)
    graph.set_entry_point("optimize")
    graph.set_finish_point("optimize")
    return graph.compile()


def create_linkedin_campaign_create_graph(operator):
    """LinkedIn campaign creation: B2B targeting → audience 50K-400K."""
    graph = StateGraph(CampaignState)
    graph.add_node("create", operator.campaign_create)
    graph.set_entry_point("create")
    graph.set_finish_point("create")
    return graph.compile()


def create_linkedin_weekly_report_graph(operator):
    """LinkedIn weekly report: CPL analysis → lead quality metrics."""
    graph = StateGraph(ReportState)
    graph.add_node("report", operator.weekly_report)
    graph.set_entry_point("report")
    graph.set_finish_point("report")
    return graph.compile()


def create_linkedin_lead_quality_review_graph(operator):
    """LinkedIn lead quality review: form rates → MQL conversion."""
    graph = StateGraph(LeadQualityState)
    graph.add_node("review", operator.lead_quality_review)
    graph.set_entry_point("review")
    graph.set_finish_point("review")
    return graph.compile()

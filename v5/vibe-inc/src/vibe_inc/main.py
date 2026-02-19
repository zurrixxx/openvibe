"""Vibe Inc runtime — wires roles, operators, and workflows."""
from openvibe_sdk import RoleRuntime

from vibe_inc.roles.d2c_growth import D2CGrowth
from vibe_inc.roles.d2c_growth.workflows import (
    create_campaign_create_graph,
    create_daily_optimize_graph,
    create_experiment_analyze_graph,
    create_funnel_diagnose_graph,
    create_page_optimize_graph,
    create_weekly_report_graph,
)


def create_runtime(llm) -> RoleRuntime:
    """Create and configure the Vibe Inc RoleRuntime.

    Registers all roles and workflow factories.
    """
    runtime = RoleRuntime(roles=[D2CGrowth], llm=llm)

    # AdOps workflows
    runtime.register_workflow("ad_ops", "campaign_create", create_campaign_create_graph)
    runtime.register_workflow("ad_ops", "daily_optimize", create_daily_optimize_graph)
    runtime.register_workflow("ad_ops", "weekly_report", create_weekly_report_graph)

    # CROps workflows
    runtime.register_workflow("cro_ops", "experiment_analyze", create_experiment_analyze_graph)
    runtime.register_workflow("cro_ops", "funnel_diagnose", create_funnel_diagnose_graph)
    runtime.register_workflow("cro_ops", "page_optimize", create_page_optimize_graph)

    return runtime

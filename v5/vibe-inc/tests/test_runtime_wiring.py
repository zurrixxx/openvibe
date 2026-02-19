from openvibe_sdk.llm import LLMResponse


class FakeLLM:
    def call(self, *, system, messages, **kwargs):
        return LLMResponse(content="done")


def test_runtime_loads_story_distributor():
    from vibe_inc.main import create_runtime

    runtime = create_runtime(llm=FakeLLM())
    role = runtime.get_role("story_distributor")
    assert role.role_id == "story_distributor"


def test_runtime_activates_daily_optimize():
    from vibe_inc.main import create_runtime

    runtime = create_runtime(llm=FakeLLM())
    result = runtime.activate(
        role_id="story_distributor",
        operator_id="ad_ops",
        workflow_id="daily_optimize",
        input_data={"date": "2026-02-19"},
    )
    assert "optimization_result" in result


def test_runtime_activates_experiment_analyze():
    from vibe_inc.main import create_runtime

    runtime = create_runtime(llm=FakeLLM())
    result = runtime.activate(
        role_id="story_distributor",
        operator_id="cro_ops",
        workflow_id="experiment_analyze",
        input_data={"product": "bot"},
    )
    assert "analysis" in result

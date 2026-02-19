from openvibe_sdk.llm import LLMResponse


class FakeLLM:
    def __init__(self, content="ok"):
        self.content = content
        self.last_system = None
        self.calls = []

    def call(self, *, system, messages, **kwargs):
        self.last_system = system
        self.calls.append({"system": system, "messages": messages, **kwargs})
        return LLMResponse(content=self.content)


def test_d2c_growth_has_operators():
    from vibe_inc.roles.d2c_growth import D2CGrowth
    assert D2CGrowth.role_id == "d2c_growth"
    op_ids = [op.operator_id for op in D2CGrowth.operators]
    assert "ad_ops" in op_ids
    assert "cro_ops" in op_ids


def test_d2c_growth_has_soul():
    from vibe_inc.roles.d2c_growth import D2CGrowth
    assert D2CGrowth.soul != ""
    assert "Net New CAC" in D2CGrowth.soul


def test_d2c_growth_get_operator():
    from vibe_inc.roles.d2c_growth import D2CGrowth

    role = D2CGrowth(llm=FakeLLM())
    ad_ops = role.get_operator("ad_ops")
    assert ad_ops.operator_id == "ad_ops"


def test_d2c_growth_soul_injected_in_prompt():
    from vibe_inc.roles.d2c_growth import D2CGrowth

    llm = FakeLLM()
    role = D2CGrowth(llm=llm)
    ad_ops = role.get_operator("ad_ops")
    ad_ops.campaign_create({"brief": {"product": "bot"}})

    # Soul should be in the system prompt
    assert "Net New CAC" in llm.last_system

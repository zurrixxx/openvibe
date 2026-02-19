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


def test_story_distributor_has_operators():
    from vibe_inc.roles.story_distributor import StoryDistributor
    assert StoryDistributor.role_id == "story_distributor"
    op_ids = [op.operator_id for op in StoryDistributor.operators]
    assert "ad_ops" in op_ids
    assert "cro_ops" in op_ids


def test_story_distributor_has_soul():
    from vibe_inc.roles.story_distributor import StoryDistributor
    assert StoryDistributor.soul != ""
    assert "Net New CAC" in StoryDistributor.soul


def test_story_distributor_get_operator():
    from vibe_inc.roles.story_distributor import StoryDistributor

    role = StoryDistributor(llm=FakeLLM())
    ad_ops = role.get_operator("ad_ops")
    assert ad_ops.operator_id == "ad_ops"


def test_story_distributor_soul_injected_in_prompt():
    from vibe_inc.roles.story_distributor import StoryDistributor

    llm = FakeLLM()
    role = StoryDistributor(llm=llm)
    ad_ops = role.get_operator("ad_ops")
    ad_ops.campaign_create({"brief": {"product": "bot"}})

    # Soul should be in the system prompt
    assert "Net New CAC" in llm.last_system

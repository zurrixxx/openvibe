from openvibe_sdk.tools import function_to_schema


def test_simple_function():
    def greet(name: str) -> str:
        """Say hello to someone."""
        return f"Hello {name}"
    schema = function_to_schema(greet)
    assert schema["name"] == "greet"
    assert schema["description"] == "Say hello to someone."
    assert schema["input_schema"]["type"] == "object"
    assert schema["input_schema"]["properties"]["name"]["type"] == "string"
    assert "name" in schema["input_schema"]["required"]


def test_multiple_params():
    def search(query: str, limit: int) -> str:
        """Search for items."""
        return ""
    schema = function_to_schema(search)
    props = schema["input_schema"]["properties"]
    assert "query" in props
    assert "limit" in props
    assert props["query"]["type"] == "string"
    assert props["limit"]["type"] == "integer"
    assert set(schema["input_schema"]["required"]) == {"query", "limit"}


def test_optional_param_with_default():
    def fetch(url: str, timeout: int = 30) -> str:
        """Fetch a URL."""
        return ""
    schema = function_to_schema(fetch)
    assert schema["input_schema"]["required"] == ["url"]
    assert "timeout" in schema["input_schema"]["properties"]


def test_bool_and_float_types():
    def configure(verbose: bool, threshold: float) -> str:
        """Configure settings."""
        return ""
    schema = function_to_schema(configure)
    props = schema["input_schema"]["properties"]
    assert props["verbose"]["type"] == "boolean"
    assert props["threshold"]["type"] == "number"


def test_no_docstring():
    def mystery(x: str) -> str:
        return x
    schema = function_to_schema(mystery)
    assert schema["description"] == ""


def test_no_type_hints_defaults_to_string():
    def untyped(x):
        """Do something."""
        return x
    schema = function_to_schema(untyped)
    assert schema["input_schema"]["properties"]["x"]["type"] == "string"

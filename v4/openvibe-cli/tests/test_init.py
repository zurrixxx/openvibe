def test_importable():
    import openvibe_cli
    assert openvibe_cli.__version__ == "0.1.0"


def test_app_has_subcommands():
    from openvibe_cli.main import app
    command_names = {cmd.name for cmd in app.registered_groups}
    assert "workspace" in command_names
    assert "role" in command_names
    assert "task" in command_names
    assert "deliverable" in command_names

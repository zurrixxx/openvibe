from unittest.mock import patch, MagicMock


def _mock_response(json_data):
    resp = MagicMock()
    resp.json.return_value = json_data
    return resp


def test_ab_test_read_lists_experiments():
    from vibe_inc.tools.optimization.ab_testing import ab_test_read

    mock_resp = _mock_response([
        {"id": 1, "name": "Bot PDP headline test", "status": "active"},
        {"id": 2, "name": "Dot CTA test", "status": "paused"},
    ])

    with patch("vibe_inc.tools.optimization.ab_testing.httpx") as mock_httpx, \
         patch("vibe_inc.tools.optimization.ab_testing._get_headers", return_value={"Authorization": "Bearer test"}), \
         patch("vibe_inc.tools.optimization.ab_testing._get_account_id", return_value="acc_123"), \
         patch("vibe_inc.tools.optimization.ab_testing._get_project_id", return_value="proj_456"):
        mock_httpx.get.return_value = mock_resp
        result = ab_test_read()

    assert "experiments" in result
    assert result["count"] == 2


def test_ab_test_read_single_experiment():
    from vibe_inc.tools.optimization.ab_testing import ab_test_read

    mock_resp = _mock_response({
        "id": 1, "name": "Bot PDP headline test", "status": "active", "variations": [],
    })

    with patch("vibe_inc.tools.optimization.ab_testing.httpx") as mock_httpx, \
         patch("vibe_inc.tools.optimization.ab_testing._get_headers", return_value={"Authorization": "Bearer test"}), \
         patch("vibe_inc.tools.optimization.ab_testing._get_account_id", return_value="acc_123"), \
         patch("vibe_inc.tools.optimization.ab_testing._get_project_id", return_value="proj_456"):
        mock_httpx.get.return_value = mock_resp
        result = ab_test_read(experiment_id="1")

    assert "experiment" in result
    assert result["experiment"]["id"] == 1


def test_ab_test_read_has_docstring():
    from vibe_inc.tools.optimization.ab_testing import ab_test_read
    assert ab_test_read.__doc__ is not None
    assert "Convert" in ab_test_read.__doc__


def test_ab_test_manage_pauses_experiment():
    from vibe_inc.tools.optimization.ab_testing import ab_test_manage

    mock_resp = _mock_response({"status": "paused"})

    with patch("vibe_inc.tools.optimization.ab_testing.httpx") as mock_httpx, \
         patch("vibe_inc.tools.optimization.ab_testing._get_headers", return_value={"Authorization": "Bearer test"}), \
         patch("vibe_inc.tools.optimization.ab_testing._get_account_id", return_value="acc_123"), \
         patch("vibe_inc.tools.optimization.ab_testing._get_project_id", return_value="proj_456"):
        mock_httpx.patch.return_value = mock_resp
        result = ab_test_manage(experiment_id="1", action="pause")

    assert result["action"] == "pause"
    assert result["experiment_id"] == "1"

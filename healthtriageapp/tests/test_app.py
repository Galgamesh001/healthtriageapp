"""
Integration tests for the Flask routes in app.py.

These mock render_template so the tests check routing/logic wiring
(which template gets chosen, what context is passed, whether the
handler raises) without depending on the actual HTML templates
existing or having specific markup. That keeps these tests fast and
decoupled from front-end changes.

Run with:  pytest -v
"""
from unittest.mock import patch
import pytest
from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


# ---------------------------------------------------------------------------
# /check — this is the route that was crashing with a NameError before the
# fix (app.py had its own duplicate check_red_flags() that called an
# undefined check_sepsis_combo()). These tests would have caught that bug
# immediately: any non-mocked call to the real check_red_flags() would
# raise, and Flask would return a 500 instead of the expected template.
# ---------------------------------------------------------------------------

def test_check_route_does_not_crash_on_plain_symptom_text(client):
    """Regression test for the NameError bug: a normal, non-red-flag
    submission must not blow up the server."""
    with patch("app.render_template", return_value="ok") as mock_render:
        response = client.post("/check", data={"symptoms": "I have a mild headache"})
    assert response.status_code == 200
    mock_render.assert_called_once()
    template_name = mock_render.call_args[0][0]
    assert template_name == "followup.html"


def test_check_route_routes_to_result_on_red_flag(client):
    with patch("app.render_template", return_value="ok") as mock_render:
        response = client.post("/check", data={"symptoms": "I have severe chest pain"})
    assert response.status_code == 200
    template_name = mock_render.call_args[0][0]
    context = mock_render.call_args[1]
    assert template_name == "result.html"
    assert context["red_flag"] is True
    assert context["red_flag_category"] == "cardiac"


def test_check_route_handles_empty_input_gracefully(client):
    with patch("app.render_template", return_value="ok"):
        response = client.post("/check", data={})
    assert response.status_code == 200


# ---------------------------------------------------------------------------
# /result
# ---------------------------------------------------------------------------

def test_result_route_urgent_for_severe(client):
    with patch("app.render_template", return_value="ok") as mock_render:
        response = client.post("/result", data={
            "symptoms_text": "some symptoms",
            "severity": "severe",
            "duration": "less_than_3",
        })
    assert response.status_code == 200
    context = mock_render.call_args[1]
    assert context["level"] == "urgent"


def test_result_route_normalizes_severity_case(client):
    """Regression test for the case-sensitivity bug: a capitalized
    severity value coming from a form must still resolve to 'urgent'."""
    with patch("app.render_template", return_value="ok") as mock_render:
        response = client.post("/result", data={
            "symptoms_text": "some symptoms",
            "severity": "Severe",
            "duration": "less_than_3",
        })
    assert response.status_code == 200
    context = mock_render.call_args[1]
    assert context["level"] == "urgent"


def test_result_route_contact_for_moderate_long_duration(client):
    with patch("app.render_template", return_value="ok") as mock_render:
        client.post("/result", data={
            "symptoms_text": "some symptoms",
            "severity": "moderate",
            "duration": "more_than_3",
        })
    context = mock_render.call_args[1]
    assert context["level"] == "contact"


def test_result_route_handles_missing_severity(client):
    """No severity field submitted at all should not crash the route."""
    with patch("app.render_template", return_value="ok") as mock_render:
        response = client.post("/result", data={"symptoms_text": "some symptoms"})
    assert response.status_code == 200
    context = mock_render.call_args[1]
    assert context["level"] == "monitor"


# ---------------------------------------------------------------------------
# / (home)
# ---------------------------------------------------------------------------

def test_home_route_renders_index(client):
    with patch("app.render_template", return_value="ok") as mock_render:
        response = client.get("/")
    assert response.status_code == 200
    mock_render.assert_called_once_with("index.html")

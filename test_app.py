"""
Unit & Integration Tests for Meeting Notes Analyzer API
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from main import app, clean_json_response

client = TestClient(app)

def test_health_endpoint():
    """Test /health endpoint returns 200 OK and status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "groq_api_key_configured" in data


def test_root_serves_html():
    """Test / endpoint serves HTML dashboard or status."""
    response = client.get("/")
    assert response.status_code == 200


def test_analyze_endpoint_validation_error():
    """Test validation error when text is too short (< 10 chars)."""
    response = client.post("/analyze", json={"text": "pendek"})
    assert response.status_code == 422 or response.status_code == 400


def test_clean_json_response_with_markdown_fence():
    """Test cleaning raw LLM response wrapped in markdown ```json ``` code fences."""
    raw = """```json
    {
        "meeting_title": "Sprint Planning",
        "summary": "Diskusi sprint baru",
        "key_points": ["Poin 1"],
        "decisions_made": ["Keputusan A"],
        "action_items": [{"task": "Buat DB", "assignee": "Budi", "deadline": "Senin", "priority": "High"}],
        "sentiment_tone": "Productive"
    }
    ```"""
    parsed = clean_json_response(raw)
    assert parsed["meeting_title"] == "Sprint Planning"
    assert len(parsed["action_items"]) == 1
    assert parsed["action_items"][0]["assignee"] == "Budi"


@patch("main.get_groq_client")
def test_analyze_meeting_success(mock_get_client):
    """Test POST /analyze with mocked Groq response."""
    mock_groq = MagicMock()
    mock_completion = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = """{
        "meeting_title": "Sprint Planning Tim Tech",
        "summary": "Rapat membahas integrasi Groq dan setup database PostgreSQL.",
        "key_points": ["Migrasi ke PostgreSQL", "Integrasi Groq API selesai minggu ini"],
        "decisions_made": ["PostgreSQL dipilih menggantikan MongoDB"],
        "action_items": [
            {
                "task": "Selesaikan endpoint /analyze",
                "assignee": "Budi",
                "deadline": "Selasa depan",
                "priority": "High"
            }
        ],
        "sentiment_tone": "Productive & Focused"
    }"""
    mock_completion.choices = [mock_choice]

    # Configure async mock
    mock_groq.chat.completions.create = AsyncMock(return_value=mock_completion)
    mock_get_client.return_value = mock_groq

    payload = {
        "text": "Meeting sprint planning tanggal 31 Oktober 2026. Budi sepakat menyelesaikan integrasi API Groq paling lambat hari Selasa. Tim memutuskan menggunakan PostgreSQL bukan MongoDB.",
        "meeting_title": "Sprint Planning Tim Tech",
        "prompt_version": "C"
    }

    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["meeting_title"] == "Sprint Planning Tim Tech"
    assert len(data["action_items"]) == 1
    assert data["action_items"][0]["assignee"] == "Budi"
    assert data["action_items"][0]["priority"] == "High"
    assert data["prompt_version_used"] == "C"

import json
from unittest.mock import patch, MagicMock
from app.llm.analyzer import analyze_match


def make_mock_client(response_dict: dict):
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text=json.dumps(response_dict))]
    mock_client = MagicMock()
    mock_client.messages.create.return_value = mock_message
    return mock_client


def test_analyze_match_returns_correct_structure():
    expected = {
        "match_score": 80,
        "match_reason": "Python 경험이 요구 사항과 잘 맞습니다.",
        "skill_gaps": ["Kubernetes"],
        "resume_suggestion": "Kubernetes 경험을 추가하세요.",
    }
    mock_client = make_mock_client(expected)
    with patch("anthropic.Anthropic", return_value=mock_client):
        result = analyze_match("이력서 내용", "공고 설명", "자격 요건")

    assert result["match_score"] == 80
    assert result["skill_gaps"] == ["Kubernetes"]
    assert result["match_reason"] == expected["match_reason"]


def test_analyze_match_score_range():
    for score in [0, 50, 100]:
        mock_client = make_mock_client({
            "match_score": score,
            "match_reason": "test",
            "skill_gaps": [],
            "resume_suggestion": "test",
        })
        with patch("anthropic.Anthropic", return_value=mock_client):
            result = analyze_match("r", "d", "q")
        assert result["match_score"] == score


def test_analyze_match_empty_skills_gap():
    mock_client = make_mock_client({
        "match_score": 95,
        "match_reason": "완벽한 매칭",
        "skill_gaps": [],
        "resume_suggestion": "현재 이력서가 적합합니다.",
    })
    with patch("anthropic.Anthropic", return_value=mock_client):
        result = analyze_match("이력서", "공고", "요건")

    assert result["skill_gaps"] == []
    assert result["match_score"] == 95

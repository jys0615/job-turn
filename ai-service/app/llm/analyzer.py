"""이력서 ↔ 공고 매칭 분석 (Claude Sonnet API)"""
import json
import anthropic
from app.core.config import settings

SYSTEM_PROMPT = """당신은 채용 전문가입니다. 이력서와 채용 공고를 분석하여 다음 JSON을 반환하세요.
반드시 JSON만 반환하고, 다른 텍스트는 포함하지 마세요.

{
  "match_score": 0~100 사이 정수,
  "match_reason": "매칭 점수의 핵심 근거 2-3문장",
  "skill_gaps": ["부족한 스킬1", "부족한 스킬2", ...],
  "resume_suggestion": "이 공고에 맞게 이력서를 고치는 구체적인 제안 2-3문장"
}"""


def analyze_match(resume_text: str, job_description: str, job_requirements: str) -> dict:
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    user_message = f"""## 이력서\n{resume_text[:3000]}\n\n## 채용 공고\n{job_description[:1500]}\n\n## 자격 요건\n{job_requirements[:1000]}"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    raw = message.content[0].text.strip()
    # Claude가 ```json ... ``` 블록으로 감쌀 경우 제거
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()
    result = json.loads(raw)

    return {
        "match_score": int(result.get("match_score", 0)),
        "match_reason": result.get("match_reason", ""),
        "skill_gaps": result.get("skill_gaps", []),
        "resume_suggestion": result.get("resume_suggestion", ""),
    }

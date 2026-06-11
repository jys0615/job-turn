# Troubleshooting Log

## 1. CI 빌드 실패 — `python-multipart` 누락

**증상**
```
RuntimeError: Form data requires "python-multipart" to be installed.
ERROR tests/test_api.py - RuntimeError
ERROR tests/test_matching_api.py - RuntimeError
```

**원인**  
FastAPI에서 multipart form data를 처리하려면 `python-multipart` 패키지가 필요한데, `requirements.txt`에 누락되어 있었음. 로컬에서는 다른 패키지의 의존성으로 간접 설치되어 있어 발견하지 못했고, CI 환경(클린 인스톨)에서만 드러남.

**해결**  
`ai-service/requirements.txt`에 추가:
```
python-multipart==0.0.12
```

---

## 2. CI 빌드 실패 — `JobServiceTest` 컴파일 에러

**증상**
```
error: cannot find symbol
    given(jobPostingRepository.search(any(), any(), any(), any()))
                              ^
symbol: method search(Object,Object,Object,Object)
```

**원인**  
`JobPostingRepository`의 단일 `search()` 메서드를 keyword/source 조합에 따라 4개 메서드(`findActive`, `searchByKeyword`, `findBySource`, `searchByKeywordAndSource`)로 분리하는 리팩토링을 했는데, `JobServiceTest`가 이전 시그니처를 참조하고 있었음.

**해결**  
`JobServiceTest`를 분리된 메서드 기준으로 재작성:
```java
// 수정 전
given(jobPostingRepository.search(any(), any(), any(), any()))

// 수정 후
given(jobPostingRepository.searchByKeyword(any(), any(), any()))
given(jobPostingRepository.findActive(any(LocalDate.class), any()))
```

---

## 3. 이력서 업로드 500 에러 — multipart 파일 크기 제한

**증상**
```json
{ "success": false, "message": "Internal server error" }
```
Spring Boot 로그:
```
Caused by: FileSizeLimitExceededException: The field file exceeds its maximum permitted
size of 1048576 bytes.
```

**원인**  
Spring Boot의 multipart 파일 크기 기본값이 1MB인데, 업로드한 이력서 PDF가 약 1.7MB여서 제한 초과.

**해결**  
`backend/src/main/resources/application.yml`에 추가:
```yaml
spring:
  servlet:
    multipart:
      max-file-size: 10MB
      max-request-size: 10MB
```

---

## 4. 매칭 분석 500 에러 — Claude JSON 파싱 실패

**증상**
```
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

**원인**  
Claude API가 JSON을 그대로 반환하지 않고 마크다운 코드블록으로 감싸서 반환하는 경우가 있음:
````
```json
{ "match_score": 72, ... }
```
````
`json.loads(raw)`가 코드블록 구문을 파싱하지 못해 실패.

**해결**  
`ai-service/app/llm/analyzer.py`에 코드블록 제거 로직 추가:
```python
if raw.startswith("```"):
    raw = raw.split("```")[1]
    if raw.startswith("json"):
        raw = raw[4:]
    raw = raw.strip()
result = json.loads(raw)
```

---

## 5. 매칭 결과 필드 전부 null — snake_case 역직렬화 실패

**증상**
```json
{
  "matchScore": 0,
  "matchReason": null,
  "skillGaps": null,
  "resumeSuggestion": null
}
```

**원인**  
FastAPI는 응답 필드명을 snake_case(`match_score`, `match_reason`, ...)로 반환하는데, Java의 `AiServiceClient.AnalysisResult` record는 camelCase(`matchScore`, `matchReason`, ...)로 선언되어 있어서 Jackson이 필드를 매핑하지 못하고 기본값(0, null)으로 역직렬화됨.

**해결**  
`AiServiceClient.AnalysisResult` record 필드에 `@JsonProperty` 추가:
```java
public record AnalysisResult(
    @JsonProperty("match_score") int matchScore,
    @JsonProperty("match_reason") String matchReason,
    @JsonProperty("skill_gaps") List<String> skillGaps,
    @JsonProperty("resume_suggestion") String resumeSuggestion
) {}
```

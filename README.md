# JobTurn

> 구직자를 위한 AI 채용 공고 분석 엔진  
> Cross-platform job matching, skill gap analysis & cover letter generation

사람인·잡코리아·원티드 공고를 통합 크롤링하고,  
내 이력서 기준으로 **매칭 점수 + 스킬 갭 + 자소서 초안**을 자동 생성하는 AI 백엔드 서비스

---

## 왜 만들었나

사람인이 2026년 5월 발표한 설문(967명)에서 직장인 **87%가 이력서 작성 중 포기**한 경험이 있고,  
포기 이유 1위는 **"공고마다 경력을 매번 수정하는 게 번거롭다"(31%)** 였다.  
<sup>출처: [AI 있어도 이직 이력서 어려워…사람인이 도와준다 — ZDNet Korea, 2026.05](https://zdnet.co.kr/view/?no=20260518081857)</sup>

국내 채용 플랫폼의 AI는 전부 **기업(채용담당자) 대상**이다.
- 잡코리아(Worxphere)는 AI 채용 매칭 플랫폼으로 리브랜딩 중<sup>[[1]](https://www.koreatimes.co.kr/business/tech-science/20260425/worxphere-ceo-on-turning-jobkorea-into-ai-led-hiring-platform)</sup>
- 원티드는 LLM 기반 채용 에이전트를 기업 대상으로 출시<sup>[[2]](https://blog.wantedlab.com/news/20251021)</sup>
- 사람인은 AI 서류합격 코칭 서비스를 출시했으나 자사 플랫폼 공고만 커버<sup>[[3]](https://zdnet.co.kr/view/?no=20260521084922)</sup>

구직자가 세 플랫폼을 동시에 쓰면서 내 이력서 기준으로 공고를 비교하고,  
무엇이 부족한지 한 곳에서 알 수 없다.

JobTurn은 그 빈틈을 채운다.

---

## 핵심 기능

| 기능 | 설명 |
|------|------|
| 크로스플랫폼 공고 수집 | 사람인·잡코리아·원티드 공고를 매 6시간 자동 크롤링 |
| 매칭 점수 + 이유 | 이력서 업로드 시 공고별 매칭 점수와 근거 반환 |
| 스킬 갭 분석 | 부족 스킬 목록과 중요도 순위 제공 |
| 공고별 이력서 diff | "이 공고엔 이렇게 고치세요" 자동 생성 |
| 자소서 초안 생성 | 문항별 맞춤 초안 SSE 스트리밍, 글자수 자동 준수 |

---

## 기술 스택

### Backend (Spring Boot)
- Java 21, Spring Boot 3.x
- Spring Security + JWT
- Spring Batch + Quartz (크롤링 파이프라인 오케스트레이션)
- WebClient (Python AI 서비스 비동기 통신)
- Kafka Producer

### AI Service (Python FastAPI)
- Python 3.12, FastAPI
- Celery + Redis (비동기 크롤링 워커)
- Playwright (사람인·잡코리아·원티드 크롤러)
- Qdrant (Dense + BM25 Hybrid Search)
- Claude Sonnet API (매칭 분석, 자소서 생성)
- pdfplumber (이력서 파싱)

### Infrastructure
- PostgreSQL, Redis, Kafka, Qdrant
- Prometheus + Grafana (Observability)
- Docker Compose → K8s (Phase 3)
- GitHub Actions CI/CD

---

## 아키텍처

```
Client
  │ HTTP / SSE
  ▼
Spring Boot (메인 백엔드)
  Auth · CRUD API · Spring Batch Orchestrator
  │ Kafka
  ▼
Python FastAPI (AI 마이크로서비스)
  매칭 엔진 (Qdrant Hybrid) · 자소서 생성 (Claude + SSE)
  │
  ├── Celery Worker: 사람인 크롤러
  ├── Celery Worker: 잡코리아 크롤러
  └── Celery Worker: 원티드 크롤러
  │
  ├── PostgreSQL (공고 · 이력서 · 분석결과)
  ├── Redis (캐시 · Celery Broker)
  └── Qdrant (벡터 DB)
```

---

## 프로젝트 구조

```
job-turn/
├── backend/                  # Spring Boot 메인 백엔드
│   └── src/main/java/com/jobturn/
│       ├── auth/             # JWT 인증
│       ├── job/              # 공고 CRUD
│       ├── resume/           # 이력서 관리
│       ├── matching/         # 매칭 결과 조회
│       ├── coverletter/      # 자소서 관리
│       └── common/           # 공통 모듈
├── ai-service/               # Python FastAPI AI 마이크로서비스
│   └── app/
│       ├── api/              # FastAPI 라우터
│       ├── crawler/          # Playwright 크롤러 (플랫폼별)
│       ├── matching/         # Qdrant Hybrid Search 매칭 엔진
│       ├── llm/              # Claude API 연동 (분석·자소서)
│       └── core/             # 설정, Celery, DB 연결
├── infra/                    # Docker Compose, Prometheus, Grafana
└── .github/workflows/        # GitHub Actions CI/CD
```

---

## 로컬 실행

```bash
# 환경변수 설정
cp .env.example .env
# .env에 ANTHROPIC_API_KEY 입력

# 전체 서비스 실행
cd infra
docker-compose up -d

# Playwright 브라우저 설치 (최초 1회)
docker exec jobturn-celery playwright install chromium
```

| 서비스 | URL |
|--------|-----|
| Spring Boot API | http://localhost:8080 |
| Swagger UI | http://localhost:8080/swagger-ui.html |
| FastAPI | http://localhost:8000 |
| FastAPI Docs | http://localhost:8000/docs |
| Grafana | http://localhost:3000 |
| Qdrant Dashboard | http://localhost:6333/dashboard |

---

## 개발 로드맵

- [x] Phase 0: 프로젝트 구조 세팅
- [ ] Phase 1 (MVP, 4주): 사람인 크롤러 + 매칭 엔진 + 스킬 갭 API
- [ ] Phase 2 (8주): 3개 플랫폼 통합 + 자소서 생성 + Observability
- [ ] Phase 3 (12주): K8s 배포 + HPA + 연봉 밴드 예측

---

## 포트폴리오 성장 포인트

이 프로젝트는 과거 프로젝트들의 숙제를 직접 답한다.

| 과거 프로젝트의 한계 | JobTurn의 답 |
|-------------------|-----------:|
| EPiC: 이기종 서버 통신 실패 시 데이터 유실 | Kafka 비동기 + Spring Batch 단계별 커밋 |
| EPiC: 테스트 코드 없이 운영 | pytest 커버리지 70%+ |
| 민들레: 동기 HTTP 오케스트레이션 한계 | Kafka로 Spring ↔ Python 완전 비동기 |
| Agent KHU: BM25 키워드 매칭 한계 | Qdrant Dense + BM25 Hybrid Search |
| Agent KHU: Docker Compose로만 운영 | K8s HPA 오토스케일링 |

---

## Author

**Jung Yoonsuh** · [GitHub](https://github.com/jys0615) · [Portfolio](https://yoonsuh.com)

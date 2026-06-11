"""
시드 데이터 삽입 스크립트
사람인 API 키 없이 개발/테스트용 공고 50건을 DB에 삽입한다.

실행: python scripts/seed_jobs.py
환경변수: DATABASE_URL (없으면 로컬 기본값 사용)
"""
import os
import psycopg2
from datetime import date, timedelta
import random

DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://jobturn:jobturn@localhost:5432/jobturn"
)

JOBS = [
    # --- 백엔드 ---
    {
        "title": "Java Spring Boot 백엔드 개발자",
        "company": "(주)카카오엔터프라이즈",
        "location": "경기 성남시",
        "description": "대용량 트래픽 처리 경험이 있는 백엔드 개발자를 모집합니다. MSA 환경에서 Spring Boot 기반 서비스를 개발하고, Kafka를 활용한 이벤트 스트리밍 시스템을 운영합니다.",
        "requirements": "Java 또는 Kotlin, Spring Boot 3년 이상, JPA/Hibernate, MySQL/PostgreSQL, Redis, Docker/K8s 경험자 우대",
        "experience_level": "경력 3~5년",
        "skills": ["Java", "Spring Boot", "Kafka", "Redis", "Kubernetes"],
    },
    {
        "title": "Python 백엔드 개발자 (FastAPI)",
        "company": "(주)당근마켓",
        "location": "서울 서초구",
        "description": "FastAPI 기반 마이크로서비스를 설계하고 개발합니다. AI/ML 서비스와 연동하는 API 서버 개발 경험을 쌓을 수 있습니다.",
        "requirements": "Python 2년 이상, FastAPI 또는 Django REST, PostgreSQL, Redis, AWS, 비동기 프로그래밍 이해",
        "experience_level": "경력 2~4년",
        "skills": ["Python", "FastAPI", "PostgreSQL", "Redis", "AWS"],
    },
    {
        "title": "Node.js 백엔드 개발자",
        "company": "(주)토스",
        "location": "서울 강남구",
        "description": "금융 서비스 백엔드를 NestJS로 개발합니다. 높은 가용성과 보안이 요구되는 핀테크 환경에서 일합니다.",
        "requirements": "Node.js, NestJS 또는 Express, TypeScript, MySQL, 보안 관련 지식, 금융/핀테크 경험 우대",
        "experience_level": "경력 3년 이상",
        "skills": ["Node.js", "NestJS", "TypeScript", "MySQL"],
    },
    {
        "title": "Go 언어 백엔드 개발자",
        "company": "(주)라인플러스",
        "location": "경기 성남시",
        "description": "Go로 고성능 메시징 시스템을 개발합니다. 수억 건의 메시지를 처리하는 글로벌 서비스 개발에 참여합니다.",
        "requirements": "Go 언어 1년 이상, gRPC, Protobuf, Kafka, 분산 시스템 이해, 영어 커뮤니케이션 가능자",
        "experience_level": "경력 3년 이상",
        "skills": ["Go", "gRPC", "Kafka", "Docker", "Kubernetes"],
    },
    {
        "title": "Spring Boot 백엔드 개발자 (신입/주니어)",
        "company": "(주)우아한형제들",
        "location": "서울 송파구",
        "description": "배달의민족 주문/결제 시스템을 담당하는 팀에서 주니어 개발자를 모집합니다.",
        "requirements": "Spring Boot, JPA, MySQL 기본 이해, 컴퓨터공학 전공 또는 관련 지식, GitHub 활동 우대",
        "experience_level": "신입 ~ 경력 2년",
        "skills": ["Java", "Spring Boot", "JPA", "MySQL", "Git"],
    },
    # --- AI / ML 엔지니어 ---
    {
        "title": "AI 서비스 백엔드 엔지니어",
        "company": "(주)네이버",
        "location": "경기 성남시",
        "description": "LLM 기반 AI 서비스의 백엔드 인프라를 설계하고 운영합니다. RAG 파이프라인, 벡터 DB 운영, Claude/GPT API 연동 경험자를 환영합니다.",
        "requirements": "Python, FastAPI, 벡터 DB(Qdrant/Pinecone/Weaviate), LangChain 또는 LlamaIndex, Docker, AWS/GCP",
        "experience_level": "경력 2~5년",
        "skills": ["Python", "FastAPI", "Qdrant", "LangChain", "AWS"],
    },
    {
        "title": "MLOps 엔지니어",
        "company": "(주)카카오브레인",
        "location": "경기 성남시",
        "description": "ML 모델 서빙 인프라를 구축하고 운영합니다. Kubeflow, MLflow, Seldon 등을 활용하여 모델 배포 파이프라인을 자동화합니다.",
        "requirements": "Python, Kubernetes, Docker, MLflow, Kubeflow, CI/CD 파이프라인 경험, ML 모델 서빙 경험",
        "experience_level": "경력 3년 이상",
        "skills": ["Python", "Kubernetes", "MLflow", "Kubeflow", "Docker"],
    },
    {
        "title": "NLP 엔지니어 (LLM 파인튜닝)",
        "company": "(주)업스테이지",
        "location": "서울 강남구",
        "description": "Solar LLM 파인튜닝 및 평가를 담당합니다. RLHF, DPO 등 최신 학습 기법을 적용하고 한국어 성능을 개선합니다.",
        "requirements": "Python, PyTorch, Transformers, 파인튜닝 경험, NLP 관련 논문 구현 능력, 영어 독해 가능",
        "experience_level": "경력 2년 이상",
        "skills": ["Python", "PyTorch", "Transformers", "LLM", "NLP"],
    },
    {
        "title": "데이터 엔지니어",
        "company": "(주)쿠팡",
        "location": "서울 강남구",
        "description": "Spark, Airflow 기반 데이터 파이프라인을 설계하고 운영합니다. 일 수십 TB 규모 데이터를 처리합니다.",
        "requirements": "Python 또는 Scala, Apache Spark, Airflow, AWS(S3/Glue/Redshift), SQL 고급, 대용량 데이터 처리 경험",
        "experience_level": "경력 3~6년",
        "skills": ["Python", "Spark", "Airflow", "AWS", "SQL"],
    },
    {
        "title": "추천 시스템 엔지니어",
        "company": "(주)왓챠",
        "location": "서울 강남구",
        "description": "콘텐츠 추천 알고리즘을 개발하고 A/B 테스트를 운영합니다. 협업 필터링, 딥러닝 기반 추천 모델을 서비스에 적용합니다.",
        "requirements": "Python, 추천 알고리즘 이해, 머신러닝 경험, Spark 또는 Flink, A/B 테스트 설계 경험",
        "experience_level": "경력 2~4년",
        "skills": ["Python", "PyTorch", "Spark", "추천시스템", "A/B테스트"],
    },
    # --- 풀스택 / 프론트엔드 ---
    {
        "title": "풀스택 개발자 (React + Spring)",
        "company": "(주)직방",
        "location": "서울 중구",
        "description": "부동산 플랫폼의 신규 서비스를 프론트부터 백엔드까지 개발합니다.",
        "requirements": "React, TypeScript, Spring Boot, PostgreSQL, AWS, REST API 설계 경험",
        "experience_level": "경력 2~5년",
        "skills": ["React", "TypeScript", "Spring Boot", "AWS"],
    },
    {
        "title": "프론트엔드 개발자 (Next.js)",
        "company": "(주)마켓컬리",
        "location": "서울 강남구",
        "description": "Next.js App Router 기반 이커머스 프론트를 개발합니다. 성능 최적화와 SEO에 관심 있는 분을 찾습니다.",
        "requirements": "React, Next.js, TypeScript, TailwindCSS, GraphQL 또는 REST, Web Vitals 최적화 경험",
        "experience_level": "경력 2~4년",
        "skills": ["React", "Next.js", "TypeScript", "GraphQL"],
    },
    # --- DevOps / 인프라 ---
    {
        "title": "DevOps 엔지니어 (AWS/K8s)",
        "company": "(주)무신사",
        "location": "서울 성동구",
        "description": "EKS 기반 컨테이너 인프라를 운영하고 CI/CD 파이프라인을 자동화합니다.",
        "requirements": "AWS(EKS, RDS, S3, CloudFront), Kubernetes, Terraform, GitHub Actions, Prometheus/Grafana",
        "experience_level": "경력 3년 이상",
        "skills": ["AWS", "Kubernetes", "Terraform", "Docker", "Prometheus"],
    },
    {
        "title": "SRE (Site Reliability Engineer)",
        "company": "(주)라인게임즈",
        "location": "서울 중구",
        "description": "게임 서비스의 가용성과 성능을 책임집니다. 장애 대응, 모니터링 시스템 구축, 인프라 자동화를 담당합니다.",
        "requirements": "Linux, Kubernetes, Prometheus, Grafana, Python 또는 Go, 장애 대응 경험, On-call 가능",
        "experience_level": "경력 3년 이상",
        "skills": ["Kubernetes", "Prometheus", "Grafana", "Python", "Linux"],
    },
    # --- 보안 ---
    {
        "title": "백엔드 보안 엔지니어",
        "company": "(주)카카오페이",
        "location": "경기 성남시",
        "description": "금융 서비스의 API 보안을 강화하고 취약점 분석 및 침투 테스트를 수행합니다.",
        "requirements": "웹 보안(OWASP Top10), Burp Suite, Spring Security, OAuth2/JWT, 금융보안 인증 경험 우대",
        "experience_level": "경력 3년 이상",
        "skills": ["Spring Security", "OAuth2", "JWT", "OWASP", "Burp Suite"],
    },
    # --- 스타트업 ---
    {
        "title": "백엔드 개발자 (초기 스타트업)",
        "company": "(주)스파르타코딩클럽",
        "location": "서울 강남구",
        "description": "교육 플랫폼의 백엔드를 Flask에서 FastAPI로 마이그레이션하고 새 기능을 개발합니다.",
        "requirements": "Python, FastAPI 또는 Flask/Django, PostgreSQL, Redis, AWS, 스타트업 환경에 익숙한 분",
        "experience_level": "경력 1~3년",
        "skills": ["Python", "FastAPI", "Django", "PostgreSQL", "AWS"],
    },
    {
        "title": "풀스택 개발자 (MVP 개발)",
        "company": "(주)팀스파르타",
        "location": "서울 강남구",
        "description": "HR Tech 스타트업에서 MVP를 빠르게 개발합니다. 기획부터 배포까지 전 과정에 참여합니다.",
        "requirements": "React 또는 Vue, Spring Boot 또는 Django, AWS, Docker, 빠른 실행력과 자기주도적 개발 성향",
        "experience_level": "경력 1~3년",
        "skills": ["React", "Spring Boot", "AWS", "Docker"],
    },
    {
        "title": "AI 백엔드 개발자 (LLM 서비스)",
        "company": "(주)뤼튼테크놀로지스",
        "location": "서울 강남구",
        "description": "GPT/Claude 기반 AI 서비스 백엔드를 개발합니다. 프롬프트 엔지니어링, RAG, 스트리밍 SSE 구현 경험자 우대.",
        "requirements": "Python, FastAPI, LangChain 또는 직접 LLM API 연동, Qdrant 또는 Pinecone, SSE/WebSocket, Redis",
        "experience_level": "경력 1~3년",
        "skills": ["Python", "FastAPI", "LangChain", "Qdrant", "Claude API"],
    },
    {
        "title": "백엔드 개발자 (헬스케어)",
        "company": "(주)눔코리아",
        "location": "서울 마포구",
        "description": "헬스케어 앱의 데이터 수집·분석 파이프라인을 개발합니다. 개인정보보호법 준수가 중요합니다.",
        "requirements": "Python 또는 Java, REST API, PostgreSQL, AWS, HIPAA/개인정보보호법 이해 우대",
        "experience_level": "경력 2~4년",
        "skills": ["Python", "AWS", "PostgreSQL", "Spring Boot"],
    },
    {
        "title": "백엔드 엔지니어 (게임 서버)",
        "company": "(주)넥슨코리아",
        "location": "경기 성남시",
        "description": "MMO 게임의 서버 사이드 로직을 C++ 또는 Java로 개발합니다. 실시간 멀티플레이어 시스템 경험자 우대.",
        "requirements": "C++ 또는 Java, 네트워크 프로그래밍, Redis, MySQL, 게임 서버 개발 경험 우대",
        "experience_level": "경력 2~5년",
        "skills": ["C++", "Java", "Redis", "MySQL", "네트워크프로그래밍"],
    },
    # --- 더 다양한 포지션 ---
    {
        "title": "클라우드 네이티브 개발자",
        "company": "(주)SK텔레콤",
        "location": "서울 중구",
        "description": "AWS/Azure 기반 클라우드 네이티브 애플리케이션을 설계하고 개발합니다.",
        "requirements": "Java 또는 Python, Spring Boot 또는 FastAPI, Kubernetes, Terraform, AWS/Azure, MSA 설계 경험",
        "experience_level": "경력 3~7년",
        "skills": ["Java", "Spring Boot", "Kubernetes", "AWS", "Terraform"],
    },
    {
        "title": "데이터 플랫폼 엔지니어",
        "company": "(주)하이퍼커넥트",
        "location": "서울 서초구",
        "description": "실시간 데이터 플랫폼(Kafka, Flink)을 운영하고 확장합니다.",
        "requirements": "Java 또는 Scala, Apache Kafka, Apache Flink 또는 Spark Streaming, AWS, 스트리밍 데이터 처리 경험",
        "experience_level": "경력 3년 이상",
        "skills": ["Kafka", "Flink", "Spark", "Java", "AWS"],
    },
    {
        "title": "백엔드 개발자 (핀테크)",
        "company": "(주)비바리퍼블리카(토스)",
        "location": "서울 강남구",
        "description": "결제·송금 서비스의 핵심 백엔드를 개발합니다. 트랜잭션 일관성과 보안이 최우선입니다.",
        "requirements": "Java, Spring Boot, JPA, MySQL, Redis, 트랜잭션 처리 이해, 금융 도메인 경험 우대",
        "experience_level": "경력 2~6년",
        "skills": ["Java", "Spring Boot", "MySQL", "Redis", "트랜잭션"],
    },
    {
        "title": "백엔드 개발자 (광고 플랫폼)",
        "company": "(주)카카오",
        "location": "경기 성남시",
        "description": "광고 입찰(RTB) 시스템의 백엔드를 개발합니다. 초저지연(< 100ms) 환경에서의 개발 경험자 우대.",
        "requirements": "Java, Spring Boot, Redis, Kafka, MySQL, 고성능 시스템 설계 경험, 광고 도메인 이해 우대",
        "experience_level": "경력 3년 이상",
        "skills": ["Java", "Kafka", "Redis", "광고플랫폼", "고성능시스템"],
    },
    {
        "title": "백엔드 개발자 (이커머스)",
        "company": "(주)SSG닷컴",
        "location": "서울 중구",
        "description": "주문·재고 관리 시스템을 개발합니다. 레거시 시스템 현대화 프로젝트에 참여합니다.",
        "requirements": "Java, Spring Boot, Oracle 또는 MySQL, Redis, MSA 전환 경험, 이커머스 도메인 이해",
        "experience_level": "경력 3~7년",
        "skills": ["Java", "Spring Boot", "Oracle", "Redis", "MSA"],
    },
    {
        "title": "백엔드 개발자 (SaaS B2B)",
        "company": "(주)플렉스",
        "location": "서울 강남구",
        "description": "HR SaaS 플랫폼의 백엔드를 개발합니다. 멀티 테넌시 아키텍처 설계 경험자 우대.",
        "requirements": "Java 또는 Python, Spring Boot 또는 Django, PostgreSQL, Redis, 멀티 테넌시 또는 SaaS 개발 경험",
        "experience_level": "경력 2~5년",
        "skills": ["Java", "Spring Boot", "PostgreSQL", "멀티테넌시", "SaaS"],
    },
    {
        "title": "검색 엔지니어 (Elasticsearch)",
        "company": "(주)네이버 쇼핑",
        "location": "경기 성남시",
        "description": "상품 검색 시스템을 Elasticsearch 기반으로 개선합니다. 형태소 분석, 랭킹 모델을 다룹니다.",
        "requirements": "Elasticsearch, Java 또는 Python, 형태소 분석(Nori), 검색 랭킹 알고리즘, 대용량 색인 경험",
        "experience_level": "경력 2~5년",
        "skills": ["Elasticsearch", "Java", "Python", "검색엔진", "NLP"],
    },
    {
        "title": "백엔드 개발자 (여행 플랫폼)",
        "company": "(주)야놀자",
        "location": "서울 강남구",
        "description": "숙박·레저 예약 시스템의 백엔드를 개발합니다. 글로벌 서비스 확장에 참여합니다.",
        "requirements": "Java, Spring Boot, MySQL, Redis, Kafka, AWS, 예약 시스템 또는 커머스 경험 우대",
        "experience_level": "경력 2~5년",
        "skills": ["Java", "Spring Boot", "Kafka", "AWS", "예약시스템"],
    },
    {
        "title": "백엔드 개발자 (교육 플랫폼)",
        "company": "(주)클래스101",
        "location": "서울 강남구",
        "description": "온라인 클래스 플랫폼의 콘텐츠 관리·결제 시스템을 개발합니다.",
        "requirements": "Python, Django 또는 FastAPI, PostgreSQL, Redis, AWS, 콘텐츠 플랫폼 경험 우대",
        "experience_level": "경력 2~4년",
        "skills": ["Python", "Django", "PostgreSQL", "AWS", "Redis"],
    },
    {
        "title": "백엔드 개발자 (물류 플랫폼)",
        "company": "(주)메쉬코리아",
        "location": "서울 강남구",
        "description": "실시간 배송 추적 및 라우팅 최적화 시스템을 개발합니다.",
        "requirements": "Python 또는 Java, PostgreSQL + PostGIS, Redis, Kafka, 위치 데이터 처리 경험 우대",
        "experience_level": "경력 2~4년",
        "skills": ["Python", "PostGIS", "Redis", "Kafka", "위치데이터"],
    },
    {
        "title": "백엔드 개발자 (스트리밍)",
        "company": "(주)아프리카TV",
        "location": "서울 강남구",
        "description": "실시간 스트리밍 서비스의 시청자 수 집계, 채팅 서버, 후원 시스템을 개발합니다.",
        "requirements": "Java 또는 Node.js, WebSocket, Redis, Kafka, MySQL, 실시간 데이터 처리 경험",
        "experience_level": "경력 2~5년",
        "skills": ["Java", "WebSocket", "Redis", "Kafka", "MySQL"],
    },
    {
        "title": "백엔드 개발자 (소셜 미디어)",
        "company": "(주)하이퍼커넥트(아자르)",
        "location": "서울 서초구",
        "description": "글로벌 소셜 앱의 매칭·채팅 백엔드를 개발합니다. 다국어, 다국가 서비스 경험자 우대.",
        "requirements": "Java 또는 Go, gRPC, Redis, Kafka, AWS, 글로벌 서비스 개발 경험, 영어 능통",
        "experience_level": "경력 3년 이상",
        "skills": ["Go", "gRPC", "Kafka", "AWS", "Redis"],
    },
    {
        "title": "백엔드 개발자 (헬스테크)",
        "company": "(주)휴레이포지티브",
        "location": "서울 마포구",
        "description": "건강 데이터 수집·분석 플랫폼을 개발합니다. IoT 디바이스 연동 경험자 우대.",
        "requirements": "Python, FastAPI, PostgreSQL, MQTT 또는 IoT 프로토콜 이해, AWS IoT, 의료 데이터 처리 경험",
        "experience_level": "경력 2~4년",
        "skills": ["Python", "FastAPI", "IoT", "MQTT", "AWS"],
    },
    {
        "title": "백엔드 개발자 (블록체인)",
        "company": "(주)카카오클레이튼",
        "location": "서울 중구",
        "description": "블록체인 노드 및 DApp 백엔드 서비스를 개발합니다.",
        "requirements": "Go 또는 Java, 블록체인 기초 이해, REST/gRPC API, PostgreSQL, AWS, Ethereum/Solidity 경험 우대",
        "experience_level": "경력 2~5년",
        "skills": ["Go", "블록체인", "Ethereum", "gRPC", "AWS"],
    },
    {
        "title": "백엔드 개발자 (모빌리티)",
        "company": "(주)카카오모빌리티",
        "location": "경기 성남시",
        "description": "택시·대리 서비스의 매칭 알고리즘 및 실시간 위치 추적 시스템을 개발합니다.",
        "requirements": "Java, Spring Boot, Redis GEO, Kafka, PostGIS, 실시간 위치 데이터 처리 경험",
        "experience_level": "경력 3~6년",
        "skills": ["Java", "Spring Boot", "Redis", "Kafka", "PostGIS"],
    },
    {
        "title": "백엔드 개발자 (B2B SaaS)",
        "company": "(주)채널코퍼레이션",
        "location": "서울 중구",
        "description": "고객 지원 플랫폼(채널톡)의 메시징 백엔드를 개발합니다. 실시간 채팅 인프라를 담당합니다.",
        "requirements": "Kotlin 또는 Java, Spring Boot, PostgreSQL, Redis, WebSocket, 대용량 메시지 처리 경험",
        "experience_level": "경력 2~5년",
        "skills": ["Kotlin", "Spring Boot", "WebSocket", "Redis", "PostgreSQL"],
    },
    {
        "title": "백엔드 개발자 (미디어)",
        "company": "(주)왓챠",
        "location": "서울 강남구",
        "description": "OTT 플랫폼의 콘텐츠 서빙, CDN 최적화, 재생 품질 개선을 담당합니다.",
        "requirements": "Python 또는 Java, CDN 이해, FFmpeg, AWS MediaConvert, PostgreSQL, Redis",
        "experience_level": "경력 2~4년",
        "skills": ["Python", "CDN", "AWS", "FFmpeg", "Redis"],
    },
    {
        "title": "백엔드 개발자 (여신금융)",
        "company": "(주)현대카드",
        "location": "서울 영등포구",
        "description": "카드 신청·심사·한도 관리 시스템의 백엔드를 현대화합니다.",
        "requirements": "Java, Spring Boot, Oracle 또는 MySQL, 금융 시스템 개발 경험, 배치 처리(Spring Batch) 경험",
        "experience_level": "경력 3~7년",
        "skills": ["Java", "Spring Boot", "Oracle", "Spring Batch", "금융"],
    },
    {
        "title": "백엔드 개발자 (의료 AI)",
        "company": "(주)루닛",
        "location": "서울 강남구",
        "description": "의료 AI 모델 결과를 병원 시스템(PACS, EMR)과 연동하는 백엔드를 개발합니다.",
        "requirements": "Python, FastAPI, DICOM 이해, PostgreSQL, Docker, AWS, HL7/FHIR 경험 우대",
        "experience_level": "경력 2~5년",
        "skills": ["Python", "FastAPI", "DICOM", "AWS", "Docker"],
    },
    {
        "title": "백엔드 개발자 (농업 플랫폼)",
        "company": "(주)그린랩스",
        "location": "서울 강남구",
        "description": "농업 데이터 수집 및 스마트팜 IoT 플랫폼 백엔드를 개발합니다.",
        "requirements": "Python, Django 또는 FastAPI, PostgreSQL, Celery, MQTT, AWS, IoT 관련 경험 우대",
        "experience_level": "경력 1~4년",
        "skills": ["Python", "Django", "Celery", "MQTT", "IoT"],
    },
    {
        "title": "백엔드 개발자 (부동산 빅데이터)",
        "company": "(주)호갱노노",
        "location": "서울 강남구",
        "description": "공공 부동산 데이터를 수집·정제·서빙하는 파이프라인과 API를 개발합니다.",
        "requirements": "Python 또는 Java, 공공데이터 API 연동 경험, PostgreSQL + PostGIS, Celery, AWS",
        "experience_level": "경력 1~3년",
        "skills": ["Python", "PostGIS", "Celery", "AWS", "공공데이터"],
    },
    {
        "title": "백엔드 개발자 (채용 플랫폼)",
        "company": "(주)원티드랩",
        "location": "서울 강남구",
        "description": "AI 채용 매칭 플랫폼의 추천 엔진과 공고 검색 시스템을 개발합니다.",
        "requirements": "Python 또는 Kotlin, FastAPI 또는 Spring Boot, Elasticsearch, Redis, PostgreSQL, 추천 시스템 경험 우대",
        "experience_level": "경력 2~4년",
        "skills": ["Python", "Elasticsearch", "Redis", "PostgreSQL", "추천시스템"],
    },
    {
        "title": "백엔드 개발자 (인사/HR 테크)",
        "company": "(주)시프티",
        "location": "서울 강남구",
        "description": "근태·급여 관리 SaaS 플랫폼의 백엔드를 개발합니다.",
        "requirements": "Ruby on Rails 또는 Python, PostgreSQL, Redis, AWS, SaaS 멀티 테넌시 경험 우대",
        "experience_level": "경력 1~4년",
        "skills": ["Ruby", "Python", "PostgreSQL", "Redis", "SaaS"],
    },
    {
        "title": "백엔드 개발자 (AI 번역)",
        "company": "(주)플리토",
        "location": "서울 마포구",
        "description": "AI 번역 API 서비스의 백엔드 및 데이터 수집 파이프라인을 개발합니다.",
        "requirements": "Python, FastAPI 또는 Flask, PostgreSQL, Celery, AWS, NLP 기초 이해, 다국어 서비스 경험 우대",
        "experience_level": "경력 1~3년",
        "skills": ["Python", "FastAPI", "Celery", "NLP", "AWS"],
    },
    {
        "title": "백엔드 개발자 (이커머스 스타트업)",
        "company": "(주)브랜디",
        "location": "서울 강남구",
        "description": "패션 이커머스 플랫폼의 상품·주문·정산 시스템을 개발합니다.",
        "requirements": "Python, Django, MySQL, Redis, Celery, AWS, 이커머스 도메인 이해",
        "experience_level": "경력 1~4년",
        "skills": ["Python", "Django", "MySQL", "Celery", "AWS"],
    },
    {
        "title": "백엔드 개발자 (리걸테크)",
        "company": "(주)로앤컴퍼니",
        "location": "서울 서초구",
        "description": "법률 정보 플랫폼(로톡)의 검색·매칭·결제 시스템을 개발합니다.",
        "requirements": "Python 또는 Java, Elasticsearch, PostgreSQL, Redis, AWS, 법률 도메인 이해 우대",
        "experience_level": "경력 2~5년",
        "skills": ["Python", "Elasticsearch", "PostgreSQL", "AWS", "Redis"],
    },
    {
        "title": "백엔드 개발자 (에듀테크)",
        "company": "(주)매스프레소(콴다)",
        "location": "서울 강남구",
        "description": "AI 수학 풀이 서비스의 문제 매칭·풀이 제공 API를 개발합니다.",
        "requirements": "Python 또는 Java, FastAPI 또는 Spring Boot, PostgreSQL, Redis, 이미지 처리 기초, AWS",
        "experience_level": "경력 2~4년",
        "skills": ["Python", "FastAPI", "PostgreSQL", "Redis", "AWS"],
    },
    {
        "title": "백엔드 개발자 (헬스케어 스타트업)",
        "company": "(주)닥터나우",
        "location": "서울 강남구",
        "description": "비대면 진료 플랫폼의 예약·진료·처방 연동 시스템을 개발합니다.",
        "requirements": "Python, Django 또는 FastAPI, PostgreSQL, Redis, AWS, 의료/헬스케어 도메인 경험 우대",
        "experience_level": "경력 2~4년",
        "skills": ["Python", "Django", "PostgreSQL", "AWS", "의료"],
    },
    {
        "title": "백엔드 개발자 (스포츠 데이터)",
        "company": "(주)스포티파이코리아",
        "location": "서울 강남구",
        "description": "스포츠 경기 데이터 수집·분석·서빙 API를 개발합니다. 실시간 스코어 업데이트 시스템을 담당합니다.",
        "requirements": "Python, FastAPI, PostgreSQL, Redis, WebSocket, AWS, 스크래핑/크롤링 경험",
        "experience_level": "경력 1~3년",
        "skills": ["Python", "FastAPI", "WebSocket", "Redis", "크롤링"],
    },
    {
        "title": "백엔드 개발자 (공유 오피스)",
        "company": "(주)패스트파이브",
        "location": "서울 강남구",
        "description": "공유 오피스 예약·결제·입주 관리 시스템의 백엔드를 개발합니다.",
        "requirements": "Java 또는 Python, Spring Boot 또는 Django, MySQL, Redis, AWS, 예약 시스템 개발 경험",
        "experience_level": "경력 2~4년",
        "skills": ["Java", "Spring Boot", "MySQL", "AWS", "예약시스템"],
    },
]


def insert_jobs(conn, jobs: list[dict]):
    cur = conn.cursor()
    inserted = 0
    today = date.today()

    for i, job in enumerate(jobs):
        expire = today + timedelta(days=random.randint(10, 60))
        external_id = f"SEED-{i+1:04d}"

        cur.execute(
            """
            INSERT INTO job_postings
                (external_id, source, title, company, location, description,
                 requirements, experience_level, expired_at, original_url, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            ON CONFLICT (external_id) DO NOTHING
            """,
            (
                external_id, "SARAMIN",
                job["title"], job["company"], job["location"],
                job["description"], job["requirements"],
                job["experience_level"], expire,
                f"https://www.saramin.co.kr/seed/{i+1}",
            ),
        )
        inserted += cur.rowcount

        # 스킬 태그 저장
        if cur.rowcount > 0:
            cur.execute("SELECT id FROM job_postings WHERE external_id = %s", (external_id,))
            job_id = cur.fetchone()[0]
            for skill in job.get("skills", []):
                cur.execute(
                    "INSERT INTO job_skills (job_id, skill) VALUES (%s, %s)",
                    (job_id, skill),
                )

    conn.commit()
    cur.close()
    return inserted


def main():
    print(f"Connecting to DB: {DB_URL.split('@')[-1]}")
    conn = psycopg2.connect(DB_URL)
    try:
        inserted = insert_jobs(conn, JOBS)
        print(f"✅ 시드 데이터 삽입 완료: {inserted}건 / 전체 {len(JOBS)}건")
    finally:
        conn.close()


if __name__ == "__main__":
    main()

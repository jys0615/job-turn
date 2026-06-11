-- Users
CREATE TABLE IF NOT EXISTS users (
    id          BIGSERIAL PRIMARY KEY,
    email       VARCHAR(255) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    name        VARCHAR(100) NOT NULL,
    created_at  TIMESTAMP    NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- Job Postings
CREATE TABLE IF NOT EXISTS job_postings (
    id               BIGSERIAL PRIMARY KEY,
    external_id      VARCHAR(255) NOT NULL UNIQUE,
    source           VARCHAR(50)  NOT NULL,
    title            VARCHAR(500) NOT NULL,
    company          VARCHAR(255) NOT NULL,
    location         VARCHAR(255),
    description      TEXT,
    requirements     TEXT,
    experience_level VARCHAR(50),
    expired_at       DATE,
    original_url     VARCHAR(1000),
    created_at       TIMESTAMP    NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_job_source  ON job_postings(source);
CREATE INDEX IF NOT EXISTS idx_job_expired ON job_postings(expired_at);

-- Job Skills (ElementCollection)
CREATE TABLE IF NOT EXISTS job_skills (
    job_id BIGINT      NOT NULL REFERENCES job_postings(id) ON DELETE CASCADE,
    skill  VARCHAR(100) NOT NULL
);

-- Resumes
CREATE TABLE IF NOT EXISTS resumes (
    id                 BIGSERIAL PRIMARY KEY,
    user_id            BIGINT       NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    original_file_name VARCHAR(500) NOT NULL,
    stored_path        VARCHAR(1000) NOT NULL,
    parsed_text        TEXT,
    content_hash       VARCHAR(64),
    created_at         TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- Match Results
CREATE TABLE IF NOT EXISTS match_results (
    id                BIGSERIAL PRIMARY KEY,
    resume_id         BIGINT   NOT NULL REFERENCES resumes(id)      ON DELETE CASCADE,
    job_id            BIGINT   NOT NULL REFERENCES job_postings(id) ON DELETE CASCADE,
    match_score       INTEGER  NOT NULL,
    match_reason      TEXT,
    resume_suggestion TEXT,
    created_at        TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_match_resume_score ON match_results(resume_id, match_score DESC);

-- Match Skill Gaps (ElementCollection)
CREATE TABLE IF NOT EXISTS match_skill_gaps (
    match_id BIGINT      NOT NULL REFERENCES match_results(id) ON DELETE CASCADE,
    skill    VARCHAR(100) NOT NULL
);

package com.jobturn.matching.repository;

import com.jobturn.matching.entity.MatchResult;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

public interface MatchResultRepository extends JpaRepository<MatchResult, Long> {
    Page<MatchResult> findByResumeIdOrderByMatchScoreDesc(Long resumeId, Pageable pageable);
}

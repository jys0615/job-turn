package com.jobturn.matching.dto;

import com.jobturn.matching.entity.MatchResult;

import java.util.List;

public record MatchResultResponse(
        Long id,
        Long jobId,
        String jobTitle,
        String company,
        Integer matchScore,
        String matchReason,
        List<String> skillGaps,
        String resumeSuggestion
) {
    public static MatchResultResponse from(MatchResult m) {
        return new MatchResultResponse(
                m.getId(),
                m.getJobPosting().getId(),
                m.getJobPosting().getTitle(),
                m.getJobPosting().getCompany(),
                m.getMatchScore(),
                m.getMatchReason(),
                m.getSkillGaps(),
                m.getResumeSuggestion()
        );
    }
}

package com.jobturn.matching.service;

import com.jobturn.common.exception.BusinessException;
import com.jobturn.job.entity.JobPosting;
import com.jobturn.job.repository.JobPostingRepository;
import com.jobturn.matching.dto.MatchResultResponse;
import com.jobturn.matching.entity.MatchResult;
import com.jobturn.matching.repository.MatchResultRepository;
import com.jobturn.resume.entity.Resume;
import com.jobturn.resume.service.ResumeService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class MatchingService {

    private final MatchResultRepository matchResultRepository;
    private final ResumeService resumeService;
    private final JobPostingRepository jobPostingRepository;
    private final AiServiceClient aiServiceClient;

    @Transactional
    public MatchResultResponse analyze(Long userId, Long resumeId, Long jobId) {
        Resume resume = resumeService.getResume(resumeId, userId);
        JobPosting job = jobPostingRepository.findById(jobId)
                .orElseThrow(() -> BusinessException.notFound("공고를 찾을 수 없습니다."));

        String resumeText = resume.getParsedText() != null ? resume.getParsedText() : "";

        AiServiceClient.AnalysisResult result = aiServiceClient
                .analyze(resumeText, job.getDescription(), job.getRequirements())
                .block();

        if (result == null) {
            throw BusinessException.badRequest("AI 분석에 실패했습니다. 잠시 후 다시 시도해주세요.");
        }

        MatchResult matchResult = MatchResult.builder()
                .resume(resume)
                .jobPosting(job)
                .matchScore(result.matchScore())
                .matchReason(result.matchReason())
                .skillGaps(result.skillGaps())
                .resumeSuggestion(result.resumeSuggestion())
                .build();

        return MatchResultResponse.from(matchResultRepository.save(matchResult));
    }

    @Transactional(readOnly = true)
    public Page<MatchResultResponse> listByResume(Long userId, Long resumeId, Pageable pageable) {
        resumeService.getResume(resumeId, userId); // ownership check
        return matchResultRepository.findByResumeIdOrderByMatchScoreDesc(resumeId, pageable)
                .map(MatchResultResponse::from);
    }
}

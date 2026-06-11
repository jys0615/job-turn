package com.jobturn.job.service;

import com.jobturn.common.exception.BusinessException;
import com.jobturn.job.dto.JobPostingResponse;
import com.jobturn.job.entity.JobPosting;
import com.jobturn.job.repository.JobPostingRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;

@Service
@RequiredArgsConstructor
public class JobService {

    private final JobPostingRepository jobPostingRepository;

    @Transactional(readOnly = true)
    public Page<JobPostingResponse> search(String keyword, String source, Pageable pageable) {
        JobPosting.JobSource jobSource = null;
        if (source != null && !source.isBlank()) {
            try {
                jobSource = JobPosting.JobSource.valueOf(source.toUpperCase());
            } catch (IllegalArgumentException e) {
                throw BusinessException.badRequest("지원하지 않는 소스입니다: " + source);
            }
        }
        return jobPostingRepository.search(keyword, jobSource, LocalDate.now(), pageable)
                .map(JobPostingResponse::from);
    }

    @Transactional(readOnly = true)
    public JobPostingResponse getById(Long id) {
        return jobPostingRepository.findById(id)
                .map(JobPostingResponse::from)
                .orElseThrow(() -> BusinessException.notFound("공고를 찾을 수 없습니다."));
    }
}

package com.jobturn.job;

import com.jobturn.common.exception.BusinessException;
import com.jobturn.job.dto.JobPostingResponse;
import com.jobturn.job.entity.JobPosting;
import com.jobturn.job.repository.JobPostingRepository;
import com.jobturn.job.service.JobService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.BDDMockito.given;

@ExtendWith(MockitoExtension.class)
class JobServiceTest {

    @Mock JobPostingRepository jobPostingRepository;
    @InjectMocks JobService jobService;

    @Test
    @DisplayName("존재하지 않는 공고 조회 시 예외")
    void getById_notFound_throws() {
        given(jobPostingRepository.findById(1L)).willReturn(Optional.empty());

        assertThatThrownBy(() -> jobService.getById(1L))
                .isInstanceOf(BusinessException.class);
    }

    @Test
    @DisplayName("공고 조회 성공")
    void getById_success() {
        JobPosting job = JobPosting.builder()
                .externalId("WN-001").source(JobPosting.JobSource.WORKNET)
                .title("백엔드 개발자").company("(주)테스트").skills(List.of("Java", "Spring"))
                .build();
        given(jobPostingRepository.findById(1L)).willReturn(Optional.of(job));

        JobPostingResponse response = jobService.getById(1L);

        assertThat(response.title()).isEqualTo("백엔드 개발자");
    }

    @Test
    @DisplayName("잘못된 source 파라미터 시 예외")
    void search_invalidSource_throws() {
        assertThatThrownBy(() ->
                jobService.search("keyword", "INVALID_SOURCE", PageRequest.of(0, 10)))
                .isInstanceOf(BusinessException.class);
    }

    @Test
    @DisplayName("공고 검색 성공")
    void search_success() {
        given(jobPostingRepository.search(any(), any(), any(), any()))
                .willReturn(new PageImpl<>(List.of()));

        var result = jobService.search("백엔드", null, PageRequest.of(0, 10));

        assertThat(result).isNotNull();
    }
}

package com.jobturn.job.controller;

import com.jobturn.common.response.ApiResponse;
import com.jobturn.job.dto.JobPostingResponse;
import com.jobturn.job.service.JobService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.web.bind.annotation.*;

@Tag(name = "Jobs", description = "채용 공고 조회")
@RestController
@RequestMapping("/api/jobs")
@RequiredArgsConstructor
public class JobController {

    private final JobService jobService;

    @Operation(summary = "공고 목록 검색")
    @GetMapping
    public ApiResponse<Page<JobPostingResponse>> search(
            @RequestParam(required = false) String keyword,
            @RequestParam(required = false) String source,
            @PageableDefault(size = 20, sort = "createdAt") Pageable pageable) {
        return ApiResponse.ok(jobService.search(keyword, source, pageable));
    }

    @Operation(summary = "공고 상세 조회")
    @GetMapping("/{id}")
    public ApiResponse<JobPostingResponse> getById(@PathVariable Long id) {
        return ApiResponse.ok(jobService.getById(id));
    }
}

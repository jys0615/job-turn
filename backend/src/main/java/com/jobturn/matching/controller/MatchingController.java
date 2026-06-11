package com.jobturn.matching.controller;

import com.jobturn.common.response.ApiResponse;
import com.jobturn.matching.dto.MatchResultResponse;
import com.jobturn.matching.service.MatchingService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

@Tag(name = "Matching", description = "이력서 ↔ 공고 매칭 분석")
@RestController
@RequestMapping("/api/resumes/{resumeId}/matches")
@RequiredArgsConstructor
public class MatchingController {

    private final MatchingService matchingService;

    @Operation(summary = "매칭 분석 요청 (AI 서비스 호출)")
    @PostMapping("/{jobId}")
    @ResponseStatus(HttpStatus.CREATED)
    public ApiResponse<MatchResultResponse> analyze(
            @AuthenticationPrincipal UserDetails userDetails,
            @PathVariable Long resumeId,
            @PathVariable Long jobId) {
        Long userId = Long.parseLong(userDetails.getUsername());
        return ApiResponse.ok(matchingService.analyze(userId, resumeId, jobId));
    }

    @Operation(summary = "이력서의 매칭 결과 목록 (점수 높은 순)")
    @GetMapping
    public ApiResponse<Page<MatchResultResponse>> list(
            @AuthenticationPrincipal UserDetails userDetails,
            @PathVariable Long resumeId,
            @PageableDefault(size = 20) Pageable pageable) {
        Long userId = Long.parseLong(userDetails.getUsername());
        return ApiResponse.ok(matchingService.listByResume(userId, resumeId, pageable));
    }
}

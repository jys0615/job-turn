package com.jobturn.resume.controller;

import com.jobturn.common.response.ApiResponse;
import com.jobturn.resume.dto.ResumeResponse;
import com.jobturn.resume.service.ResumeService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

@Tag(name = "Resume", description = "이력서 업로드 / 조회")
@RestController
@RequestMapping("/api/resumes")
@RequiredArgsConstructor
public class ResumeController {

    private final ResumeService resumeService;

    @Operation(summary = "이력서 업로드 (PDF)")
    @PostMapping(consumes = "multipart/form-data")
    @ResponseStatus(HttpStatus.CREATED)
    public ApiResponse<ResumeResponse> upload(
            @AuthenticationPrincipal UserDetails userDetails,
            @RequestParam("file") MultipartFile file) throws IOException {
        Long userId = Long.parseLong(userDetails.getUsername());
        return ApiResponse.ok(resumeService.upload(userId, file));
    }

    @Operation(summary = "내 이력서 목록")
    @GetMapping
    public ApiResponse<List<ResumeResponse>> list(
            @AuthenticationPrincipal UserDetails userDetails) {
        Long userId = Long.parseLong(userDetails.getUsername());
        return ApiResponse.ok(resumeService.listByUser(userId));
    }
}

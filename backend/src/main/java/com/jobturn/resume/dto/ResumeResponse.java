package com.jobturn.resume.dto;

import com.jobturn.resume.entity.Resume;

import java.time.LocalDateTime;

public record ResumeResponse(
        Long id,
        String originalFileName,
        String contentHash,
        LocalDateTime createdAt
) {
    public static ResumeResponse from(Resume resume) {
        return new ResumeResponse(
                resume.getId(),
                resume.getOriginalFileName(),
                resume.getContentHash(),
                resume.getCreatedAt()
        );
    }
}

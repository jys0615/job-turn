package com.jobturn.job.dto;

import com.jobturn.job.entity.JobPosting;

import java.time.LocalDate;
import java.util.List;

public record JobPostingResponse(
        Long id,
        String externalId,
        String source,
        String title,
        String company,
        String location,
        String description,
        String requirements,
        String experienceLevel,
        LocalDate expiredAt,
        String originalUrl,
        List<String> skills
) {
    public static JobPostingResponse from(JobPosting job) {
        return new JobPostingResponse(
                job.getId(), job.getExternalId(), job.getSource().name(),
                job.getTitle(), job.getCompany(), job.getLocation(),
                job.getDescription(), job.getRequirements(), job.getExperienceLevel(),
                job.getExpiredAt(), job.getOriginalUrl(), job.getSkills()
        );
    }
}

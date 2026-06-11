package com.jobturn.job.entity;

import jakarta.persistence.*;
import lombok.*;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

@Entity
@Table(name = "job_postings", indexes = {
        @Index(name = "idx_job_source", columnList = "source"),
        @Index(name = "idx_job_expired", columnList = "expiredAt")
})
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@EntityListeners(AuditingEntityListener.class)
public class JobPosting {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String externalId;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private JobSource source;

    @Column(nullable = false)
    private String title;

    @Column(nullable = false)
    private String company;

    private String location;

    @Column(columnDefinition = "TEXT")
    private String description;

    @Column(columnDefinition = "TEXT")
    private String requirements;

    private String experienceLevel;

    private LocalDate expiredAt;

    private String originalUrl;

    @ElementCollection
    @CollectionTable(name = "job_skills", joinColumns = @JoinColumn(name = "job_id"))
    @Column(name = "skill")
    private List<String> skills;

    @CreatedDate
    @Column(updatable = false)
    private LocalDateTime createdAt;

    @Builder
    public JobPosting(String externalId, JobSource source, String title, String company,
                      String location, String description, String requirements,
                      String experienceLevel, LocalDate expiredAt, String originalUrl,
                      List<String> skills) {
        this.externalId = externalId;
        this.source = source;
        this.title = title;
        this.company = company;
        this.location = location;
        this.description = description;
        this.requirements = requirements;
        this.experienceLevel = experienceLevel;
        this.expiredAt = expiredAt;
        this.originalUrl = originalUrl;
        this.skills = skills;
    }

    public enum JobSource {
        WORKNET, SARAMIN, JOBKOREA, WANTED
    }
}

package com.jobturn.matching.entity;

import com.jobturn.job.entity.JobPosting;
import com.jobturn.resume.entity.Resume;
import jakarta.persistence.*;
import lombok.*;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.LocalDateTime;
import java.util.List;

@Entity
@Table(name = "match_results", indexes = {
        @Index(name = "idx_match_resume_score", columnList = "resume_id, matchScore DESC")
})
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@EntityListeners(AuditingEntityListener.class)
public class MatchResult {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "resume_id", nullable = false)
    private Resume resume;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "job_id", nullable = false)
    private JobPosting jobPosting;

    @Column(nullable = false)
    private Integer matchScore;

    @Column(columnDefinition = "TEXT")
    private String matchReason;

    @ElementCollection
    @CollectionTable(name = "match_skill_gaps", joinColumns = @JoinColumn(name = "match_id"))
    @Column(name = "skill")
    private List<String> skillGaps;

    @Column(columnDefinition = "TEXT")
    private String resumeSuggestion;

    @CreatedDate
    @Column(updatable = false)
    private LocalDateTime createdAt;

    @Builder
    public MatchResult(Resume resume, JobPosting jobPosting, Integer matchScore,
                       String matchReason, List<String> skillGaps, String resumeSuggestion) {
        this.resume = resume;
        this.jobPosting = jobPosting;
        this.matchScore = matchScore;
        this.matchReason = matchReason;
        this.skillGaps = skillGaps;
        this.resumeSuggestion = resumeSuggestion;
    }
}

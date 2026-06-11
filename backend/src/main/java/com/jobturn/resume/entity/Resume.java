package com.jobturn.resume.entity;

import com.jobturn.auth.entity.User;
import jakarta.persistence.*;
import lombok.*;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.LocalDateTime;

@Entity
@Table(name = "resumes")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@EntityListeners(AuditingEntityListener.class)
public class Resume {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @Column(nullable = false)
    private String originalFileName;

    @Column(nullable = false)
    private String storedPath;

    @Column(columnDefinition = "TEXT")
    private String parsedText;

    private String contentHash;

    @CreatedDate
    @Column(updatable = false)
    private LocalDateTime createdAt;

    @Builder
    public Resume(User user, String originalFileName, String storedPath,
                  String parsedText, String contentHash) {
        this.user = user;
        this.originalFileName = originalFileName;
        this.storedPath = storedPath;
        this.parsedText = parsedText;
        this.contentHash = contentHash;
    }
}

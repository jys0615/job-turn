package com.jobturn.resume.repository;

import com.jobturn.resume.entity.Resume;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface ResumeRepository extends JpaRepository<Resume, Long> {
    List<Resume> findByUserIdOrderByCreatedAtDesc(Long userId);
    Optional<Resume> findByIdAndUserId(Long id, Long userId);
}

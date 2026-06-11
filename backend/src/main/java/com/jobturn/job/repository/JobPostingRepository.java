package com.jobturn.job.repository;

import com.jobturn.job.entity.JobPosting;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDate;
import java.util.Optional;

public interface JobPostingRepository extends JpaRepository<JobPosting, Long> {

    Optional<JobPosting> findByExternalId(String externalId);

    boolean existsByExternalId(String externalId);

    @Query("SELECT j FROM JobPosting j WHERE " +
           "(:keyword IS NULL OR LOWER(j.title) LIKE LOWER(CONCAT('%', :keyword, '%')) " +
           "   OR LOWER(j.company) LIKE LOWER(CONCAT('%', :keyword, '%'))) " +
           "AND (:source IS NULL OR j.source = :source) " +
           "AND (j.expiredAt IS NULL OR j.expiredAt >= :today)")
    Page<JobPosting> search(
            @Param("keyword") String keyword,
            @Param("source") JobPosting.JobSource source,
            @Param("today") LocalDate today,
            Pageable pageable);
}

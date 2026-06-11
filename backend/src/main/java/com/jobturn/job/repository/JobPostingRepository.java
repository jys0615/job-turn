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

    // keyword 없을 때
    @Query("SELECT j FROM JobPosting j WHERE j.expiredAt IS NULL OR j.expiredAt >= :today")
    Page<JobPosting> findActive(@Param("today") LocalDate today, Pageable pageable);

    // keyword 있을 때
    @Query("SELECT j FROM JobPosting j WHERE " +
           "(LOWER(j.title) LIKE LOWER(CONCAT('%', :keyword, '%')) " +
           " OR LOWER(j.company) LIKE LOWER(CONCAT('%', :keyword, '%'))) " +
           "AND (j.expiredAt IS NULL OR j.expiredAt >= :today)")
    Page<JobPosting> searchByKeyword(
            @Param("keyword") String keyword,
            @Param("today") LocalDate today,
            Pageable pageable);

    // source 필터
    @Query("SELECT j FROM JobPosting j WHERE j.source = :source " +
           "AND (j.expiredAt IS NULL OR j.expiredAt >= :today)")
    Page<JobPosting> findBySource(
            @Param("source") JobPosting.JobSource source,
            @Param("today") LocalDate today,
            Pageable pageable);

    // keyword + source 필터
    @Query("SELECT j FROM JobPosting j WHERE " +
           "(LOWER(j.title) LIKE LOWER(CONCAT('%', :keyword, '%')) " +
           " OR LOWER(j.company) LIKE LOWER(CONCAT('%', :keyword, '%'))) " +
           "AND j.source = :source " +
           "AND (j.expiredAt IS NULL OR j.expiredAt >= :today)")
    Page<JobPosting> searchByKeywordAndSource(
            @Param("keyword") String keyword,
            @Param("source") JobPosting.JobSource source,
            @Param("today") LocalDate today,
            Pageable pageable);
}

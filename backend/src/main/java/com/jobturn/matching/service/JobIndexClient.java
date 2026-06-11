package com.jobturn.matching.service;

import com.jobturn.job.entity.JobPosting;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.Map;

@Slf4j
@Component
public class JobIndexClient {

    private final WebClient webClient;

    public JobIndexClient(@Value("${ai-service.url}") String baseUrl) {
        this.webClient = WebClient.builder().baseUrl(baseUrl).build();
    }

    public void index(JobPosting job) {
        Map<String, Object> body = Map.of(
                "job_id", job.getId(),
                "title", job.getTitle(),
                "company", job.getCompany(),
                "description", job.getDescription() != null ? job.getDescription() : "",
                "requirements", job.getRequirements() != null ? job.getRequirements() : ""
        );
        webClient.post()
                .uri("/api/jobs/index")
                .bodyValue(body)
                .retrieve()
                .bodyToMono(Void.class)
                .doOnError(e -> log.warn("Job index failed: {}", e.getMessage()))
                .onErrorComplete()
                .subscribe();
    }
}

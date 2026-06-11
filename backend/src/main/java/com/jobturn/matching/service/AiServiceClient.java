package com.jobturn.matching.service;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.util.List;
import java.util.Map;

@Slf4j
@Component
public class AiServiceClient {

    private final WebClient webClient;

    public AiServiceClient(@Value("${ai-service.url}") String baseUrl) {
        this.webClient = WebClient.builder().baseUrl(baseUrl).build();
    }

    public Mono<AnalysisResult> analyze(String resumeText, String jobDescription, String jobRequirements) {
        Map<String, String> body = Map.of(
                "resume_text", resumeText,
                "job_description", jobDescription,
                "job_requirements", jobRequirements
        );
        return webClient.post()
                .uri("/api/analyze")
                .bodyValue(body)
                .retrieve()
                .bodyToMono(AnalysisResult.class)
                .doOnError(e -> log.error("AI service error: {}", e.getMessage()));
    }

    public record AnalysisResult(
            int matchScore,
            String matchReason,
            List<String> skillGaps,
            String resumeSuggestion
    ) {}
}

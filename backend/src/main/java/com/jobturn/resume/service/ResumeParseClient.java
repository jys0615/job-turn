package com.jobturn.resume.service;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.MediaType;
import org.springframework.http.client.MultipartBodyBuilder;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;

@Slf4j
@Component
public class ResumeParseClient {

    private final WebClient webClient;

    public ResumeParseClient(@Value("${ai-service.url}") String baseUrl) {
        this.webClient = WebClient.builder().baseUrl(baseUrl).build();
    }

    public String parse(byte[] pdfBytes, String fileName) {
        MultipartBodyBuilder builder = new MultipartBodyBuilder();
        builder.part("file", new ByteArrayResource(pdfBytes) {
            @Override
            public String getFilename() {
                return fileName;
            }
        }).contentType(MediaType.APPLICATION_PDF);

        try {
            ParseResult result = webClient.post()
                    .uri("/api/resume/parse")
                    .contentType(MediaType.MULTIPART_FORM_DATA)
                    .body(BodyInserters.fromMultipartData(builder.build()))
                    .retrieve()
                    .bodyToMono(ParseResult.class)
                    .block();
            return result != null ? result.raw() : "";
        } catch (Exception e) {
            log.warn("Resume parse failed, storing without parsed text: {}", e.getMessage());
            return "";
        }
    }

    record ParseResult(String raw, String summary, String experience,
                       String skills, String education, String projects) {}
}

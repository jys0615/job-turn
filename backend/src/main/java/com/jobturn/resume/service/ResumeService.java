package com.jobturn.resume.service;

import com.jobturn.auth.entity.User;
import com.jobturn.auth.repository.UserRepository;
import com.jobturn.common.exception.BusinessException;
import com.jobturn.resume.dto.ResumeResponse;
import com.jobturn.resume.entity.Resume;
import com.jobturn.resume.repository.ResumeRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.HexFormat;
import java.util.List;

@Service
@RequiredArgsConstructor
public class ResumeService {

    private final ResumeRepository resumeRepository;
    private final UserRepository userRepository;
    private final ResumeParseClient resumeParseClient;

    @Value("${resume.storage-path:./uploads/resumes}")
    private String storagePath;

    @Transactional
    public ResumeResponse upload(Long userId, MultipartFile file) throws IOException {
        validatePdf(file);
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new UsernameNotFoundException("User not found"));

        byte[] bytes = file.getBytes();
        String hash = md5(bytes);

        Path dir = Paths.get(storagePath, String.valueOf(userId));
        Files.createDirectories(dir);
        Path dest = dir.resolve(hash + ".pdf");
        Files.write(dest, bytes);

        // AI 서비스로 PDF 파싱 (실패해도 업로드는 성공)
        String parsedText = resumeParseClient.parse(bytes, file.getOriginalFilename());

        Resume resume = Resume.builder()
                .user(user)
                .originalFileName(file.getOriginalFilename())
                .storedPath(dest.toString())
                .parsedText(parsedText)
                .contentHash(hash)
                .build();
        return ResumeResponse.from(resumeRepository.save(resume));
    }

    @Transactional(readOnly = true)
    public List<ResumeResponse> listByUser(Long userId) {
        return resumeRepository.findByUserIdOrderByCreatedAtDesc(userId)
                .stream().map(ResumeResponse::from).toList();
    }

    @Transactional(readOnly = true)
    public Resume getResume(Long resumeId, Long userId) {
        return resumeRepository.findByIdAndUserId(resumeId, userId)
                .orElseThrow(() -> BusinessException.notFound("이력서를 찾을 수 없습니다."));
    }

    private void validatePdf(MultipartFile file) {
        if (file.isEmpty()) throw BusinessException.badRequest("파일이 비어 있습니다.");
        String name = file.getOriginalFilename();
        if (name == null || !name.toLowerCase().endsWith(".pdf")) {
            throw BusinessException.badRequest("PDF 파일만 업로드할 수 있습니다.");
        }
    }

    private String md5(byte[] data) {
        try {
            MessageDigest md = MessageDigest.getInstance("MD5");
            return HexFormat.of().formatHex(md.digest(data));
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        }
    }
}

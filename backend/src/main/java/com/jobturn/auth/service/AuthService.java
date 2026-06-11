package com.jobturn.auth.service;

import com.jobturn.auth.dto.LoginRequest;
import com.jobturn.auth.dto.SignupRequest;
import com.jobturn.auth.dto.TokenResponse;
import com.jobturn.auth.entity.User;
import com.jobturn.auth.repository.UserRepository;
import com.jobturn.common.exception.BusinessException;
import com.jobturn.common.util.JwtUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtUtil jwtUtil;

    @Transactional
    public void signup(SignupRequest request) {
        if (userRepository.existsByEmail(request.email())) {
            throw BusinessException.badRequest("이미 사용 중인 이메일입니다.");
        }
        userRepository.save(User.builder()
                .email(request.email())
                .password(passwordEncoder.encode(request.password()))
                .name(request.name())
                .build());
    }

    @Transactional(readOnly = true)
    public TokenResponse login(LoginRequest request) {
        User user = userRepository.findByEmail(request.email())
                .orElseThrow(() -> BusinessException.unauthorized("이메일 또는 비밀번호가 올바르지 않습니다."));
        if (!passwordEncoder.matches(request.password(), user.getPassword())) {
            throw BusinessException.unauthorized("이메일 또는 비밀번호가 올바르지 않습니다.");
        }
        return TokenResponse.of(
                jwtUtil.generateAccessToken(user.getId(), user.getEmail()),
                jwtUtil.generateRefreshToken(user.getId(), user.getEmail())
        );
    }
}

package com.jobturn.auth;

import com.jobturn.auth.dto.LoginRequest;
import com.jobturn.auth.dto.SignupRequest;
import com.jobturn.auth.dto.TokenResponse;
import com.jobturn.auth.entity.User;
import com.jobturn.auth.repository.UserRepository;
import com.jobturn.auth.service.AuthService;
import com.jobturn.common.exception.BusinessException;
import com.jobturn.common.util.JwtUtil;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.verify;

@ExtendWith(MockitoExtension.class)
class AuthServiceTest {

    @Mock UserRepository userRepository;
    @Mock PasswordEncoder passwordEncoder;
    @Mock JwtUtil jwtUtil;
    @InjectMocks AuthService authService;

    @Test
    @DisplayName("이메일 중복 시 예외 발생")
    void signup_duplicateEmail_throws() {
        given(userRepository.existsByEmail("test@test.com")).willReturn(true);

        assertThatThrownBy(() -> authService.signup(new SignupRequest("test@test.com", "pass1234", "홍길동")))
                .isInstanceOf(BusinessException.class);
    }

    @Test
    @DisplayName("회원가입 성공 시 save 호출")
    void signup_success() {
        given(userRepository.existsByEmail(any())).willReturn(false);
        given(passwordEncoder.encode(any())).willReturn("encoded");

        authService.signup(new SignupRequest("test@test.com", "pass1234", "홍길동"));

        verify(userRepository).save(any(User.class));
    }

    @Test
    @DisplayName("비밀번호 불일치 시 예외 발생")
    void login_wrongPassword_throws() {
        User user = User.builder().email("test@test.com").password("encoded").name("홍길동").build();
        given(userRepository.findByEmail("test@test.com")).willReturn(Optional.of(user));
        given(passwordEncoder.matches("wrongpw", "encoded")).willReturn(false);

        assertThatThrownBy(() -> authService.login(new LoginRequest("test@test.com", "wrongpw")))
                .isInstanceOf(BusinessException.class);
    }

    @Test
    @DisplayName("로그인 성공 시 TokenResponse 반환")
    void login_success() {
        User user = User.builder().email("test@test.com").password("encoded").name("홍길동").build();
        given(userRepository.findByEmail("test@test.com")).willReturn(Optional.of(user));
        given(passwordEncoder.matches("pass1234", "encoded")).willReturn(true);
        given(jwtUtil.generateAccessToken(any(), any())).willReturn("access-token");
        given(jwtUtil.generateRefreshToken(any(), any())).willReturn("refresh-token");

        TokenResponse response = authService.login(new LoginRequest("test@test.com", "pass1234"));

        assertThat(response.accessToken()).isEqualTo("access-token");
        assertThat(response.tokenType()).isEqualTo("Bearer");
    }
}

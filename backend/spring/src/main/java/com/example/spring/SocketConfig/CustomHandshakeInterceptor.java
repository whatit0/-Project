package com.example.spring.SocketConfig;

import java.util.Map;

import org.springframework.http.server.ServerHttpRequest;
import org.springframework.http.server.ServerHttpResponse;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.WebSocketHandler;
import org.springframework.web.socket.server.HandshakeInterceptor;

import com.example.spring.security.JwtAuthenticationProvider;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Component
public class CustomHandshakeInterceptor implements HandshakeInterceptor {

    private final JwtAuthenticationProvider jwtTokenProvider;
    @Override
    public boolean beforeHandshake(ServerHttpRequest request, ServerHttpResponse response, WebSocketHandler wsHandler, Map<String, Object> attributes) throws Exception {
        // "Authorization" 헤더에서 JWT 토큰 추출
        String token = request.getHeaders().getFirst("Authorization");
        if (token != null && token.startsWith("Bearer ")) {
            token = token.substring(7); // "Bearer " 접두사 제거
        }

        // JWT 토큰 검증 및 사용자 정보 추출
        Authentication authentication = jwtTokenProvider.getAuthentication(token);
        String userId = (String) authentication.getPrincipal();

        // WebSocket 세션 속성에 사용자 정보 저장
        attributes.put("userId", userId);

        return true;
    }

    @Override
    public void afterHandshake(ServerHttpRequest request, ServerHttpResponse response, WebSocketHandler wsHandler, Exception exception) {
        // 후처리 로직 (필요한 경우)
    }
}

package com.example.spring.config;

import com.example.spring.security.JwtAuthenticationProvider;
import lombok.RequiredArgsConstructor;
import org.springframework.http.server.ServerHttpRequest;
import org.springframework.http.server.ServerHttpResponse;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.WebSocketHandler;
import org.springframework.web.socket.server.HandshakeInterceptor;

import java.util.Map;

@RequiredArgsConstructor
@Component
public class CustomHandshakeInterceptor implements HandshakeInterceptor {

    private final JwtAuthenticationProvider jwtTokenProvider;

    @Override
    public boolean beforeHandshake(ServerHttpRequest request, ServerHttpResponse response, WebSocketHandler wsHandler, Map<String, Object> attributes) throws Exception {
        String token = request.getURI().getQuery().split("access_token=")[1];
        if (token != null && !token.trim().isEmpty()) {
            if (token.startsWith("Bearer ")) {
                token = token.substring(7); // "Bearer " 접두사 제거
            }
            try {
                Authentication authentication = jwtTokenProvider.getAuthentication(token);
                if (authentication != null) {
                    String userId = (String) authentication.getPrincipal();
                    attributes.put("userId", userId);
                    return true;
                }
            } catch (Exception e) {
                System.out.println("WebSocket 연결 실패: JWT 토큰 검증 중 오류가 발생했습니다. 오류 메시지: " + e.getMessage());
                return false;
            }
        } else {
            System.out.println("WebSocket 연결 실패: JWT 토큰이 없습니다.");
            return false;
        }
        return false;
    }

    @Override
        public void afterHandshake(ServerHttpRequest request, ServerHttpResponse response, WebSocketHandler wsHandler, Exception exception) {
            // 후처리 로직 (필요한 경우)
        }
}

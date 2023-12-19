package com.example.spring.security;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jws;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import lombok.extern.log4j.Log4j2;
import org.springframework.security.authentication.AuthenticationProvider;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.stereotype.Component;

import java.security.SecureRandom;
import java.util.*;

@Log4j2
@Component
public class JwtAuthenticationProvider {


    private static final String SECRET_KEY = "your_secret_key";  // 환경 변수나 설정 파일에서 가져오는 것이 바람직


//    @Override
//    public Authentication authenticate(Authentication authentication) throws AuthenticationException {
//        log.warn("implement later");
//        return null;
//    }
//
//    @Override
//    public boolean supports(Class<?> authentication) {
//        log.warn("implement later");
//        return false;
//    }
    // jwt 토큰 생성
    public Map<String, Object> createToken(String userId, String userNickname) {
        Claims claims = Jwts.claims();
        claims.put("Id",userId);
        claims.put("NickName", userNickname);
        Date now = new Date();
        long validityInMilliseconds = 3600000; // 1시간
        Date validity = new Date(now.getTime() + validityInMilliseconds);
        String token = Jwts.builder()
                .setClaims(claims)
                .setIssuedAt(now)
                .setExpiration(new Date(now.getTime() + 3600000))
                .signWith(SignatureAlgorithm.HS256, generateKey())
                .compact();

        Map<String, Object> tokenData = new HashMap<>();
        tokenData.put("accessToken", token);
        tokenData.put("expiresIn", validityInMilliseconds/1000);  // 초 단위로 저장
        return tokenData;
    }

////     jwt refresh 토큰 기능 비활성화
//    public String createRefreshToken() {
//        Date now = new Date();
//        return Jwts.builder()
//                .setIssuedAt(now)
//                .setExpiration(new Date(now.getTime() + 3600000))
//                .signWith(SignatureAlgorithm.HS256, generateKey())
//                .compact();
//    }

    public static String generateKey() {
        SecureRandom random = new SecureRandom();
        byte[] key = new byte[32]; // 256비트 키
        random.nextBytes(key);
//        return Base64.getEncoder().encodeToString(key);
        return SECRET_KEY;
    }

    // 사용자 인증 정보를 생성하는 메소드
    public Authentication getAuthentication(String token) {
        String secretKey = JwtAuthenticationProvider.generateKey();
        Jws<Claims> claims = Jwts.parser()
                .setSigningKey(secretKey.getBytes())
                .parseClaimsJws(token);

        // JWT 토큰에서 사용자 정보 추출
        String userId = claims.getBody().getSubject();
        String userNickname = claims.getBody().get("NickName", String.class);

        // 디코딩된 정보를 기반으로 Authentication 객체 생성
        return new UsernamePasswordAuthenticationToken(userId, null,
                Collections.singletonList(new SimpleGrantedAuthority("ROLE_USER")));
    }
}

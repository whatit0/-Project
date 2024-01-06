package com.example.spring.security;
import lombok.Getter;
import org.springframework.security.authentication.AbstractAuthenticationToken;
import org.springframework.security.core.GrantedAuthority;

import java.util.Collection;

@Getter
public class JwtAuthenticationToken extends AbstractAuthenticationToken {

    private String jsonWebToken;
    private Object principal;
    private Object credentials;


    // HTTP의 요청의 헤더에서 JWT 추출
    public JwtAuthenticationToken(String jsonWebToken) {
        super(null);
        this.jsonWebToken = jsonWebToken;
        // 인증 권한 : null 로 지정
        this.setAuthenticated(false);
        // 받은 토큰은 인증되지 않은 상태로 초기화
    }

    public JwtAuthenticationToken(Object principal, Object credentials, Collection<? extends GrantedAuthority> authorities) {
        super(authorities);
        this.principal = principal;
        this.credentials = credentials;
        super.setAuthenticated(true);
        // 토큰을 인증 받은 상태로 설정
    }

}

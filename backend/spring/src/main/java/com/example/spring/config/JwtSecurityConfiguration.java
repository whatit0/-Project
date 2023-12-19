package com.example.spring.config;

import com.example.spring.security.JwtAuthenticationFilter;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.SecurityConfigurerAdapter;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.DefaultSecurityFilterChain;
import org.springframework.security.web.authentication.logout.LogoutFilter;

@Configuration
public class JwtSecurityConfiguration extends SecurityConfigurerAdapter<DefaultSecurityFilterChain, HttpSecurity> {

    // private final AuthenticationManager authenticationManager;

    // public JwtSecurityConfiguration(AuthenticationManager authenticationManager) {
    //     this.authenticationManager = authenticationManager;
    // }

    @Override
    public void configure(HttpSecurity http) throws Exception {
        JwtAuthenticationFilter jwtFilter = new JwtAuthenticationFilter();
        http.addFilterAfter(jwtFilter, LogoutFilter.class);
    }
}

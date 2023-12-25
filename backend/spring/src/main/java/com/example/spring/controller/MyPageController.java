package com.example.spring.controller;

import com.example.spring.dto.BoardDto;
import com.example.spring.security.JwtAuthenticationProvider;
import com.example.spring.service.BoardService;
import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.PropertySource;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@RestController
@RequiredArgsConstructor
@PropertySource("classpath:application.properties")
@CrossOrigin(origins = "http://localhost:3000", methods = {RequestMethod.GET, RequestMethod.POST}, allowCredentials = "true")
@RequestMapping("/public/mypage")
public class MyPageController {

    private final JwtAuthenticationProvider jwtTokenProvider;
    private final BoardService boardService;



    @PostMapping("/mypagerequest")
    public ResponseEntity<?> myPageRequest(HttpServletRequest request) {

        String accessToken = request.getHeader("Authorization");
        if (accessToken != null && accessToken.startsWith("Bearer ")) {
            accessToken = accessToken.substring(7);
        }

        try {
            Authentication authentication = jwtTokenProvider.getAuthentication(accessToken);
            String userId = (String) authentication.getPrincipal();

            // ID를 포함한 어떤 객체를 생성하여 리턴합니다. 여기서는 단순히 ID만 리턴합니다.
            return ResponseEntity.ok().body(userId);
        } catch (Exception e) {
            // 토큰이 유효하지 않을 경우의 처리를 여기서 합니다.
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Invalid token");
        }
    }


    @PostMapping("/myboardlist")
    public List<BoardDto> BoardSearch(@RequestParam("userid") String userId) {
        List<BoardDto> boardDtos = boardService.boardFindUserid(userId);
        System.out.println(boardDtos);
        return boardDtos;}
//        return boardService.boardFindUserid(userId);}



}
package com.example.spring.controller;

import com.example.spring.dto.UserDto;
import com.example.spring.entity.UserEntity;
import com.example.spring.repository.UserRepository;
import com.example.spring.security.JwtAuthenticationProvider;
import com.example.spring.service.UserService;
import jakarta.servlet.http.HttpSession;
import org.hibernate.annotations.Check;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.annotation.Secured;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@CrossOrigin(origins = "http://localhost:3000", methods = {RequestMethod.GET, RequestMethod.POST},  allowCredentials = "true")
// port 간 통신에서 CORS를 막기 위한 설정
public class UserController {


    private final UserService userService;
    private JwtAuthenticationProvider jwtTokenProvider;


    @Autowired
    private UserRepository userRepository; // 사용자 정보를 저장하는 리포지토리

    @Autowired
    public UserController(UserService userService, JwtAuthenticationProvider jwtTokenProvider) {
        this.userService = userService;
        this.jwtTokenProvider = jwtTokenProvider;
    }


    @PostMapping("/public/loginPageRequest")
    public String loginPage(){
        return "abcd";
    }

    // http://localhost:8080/user/loginRequest
    @PostMapping("/public/loginRequest")
    public ResponseEntity<String> loginRequest(@RequestBody Map<String, String> requestBody, HttpSession session) {
        String userId = requestBody.get("userId");
        String userPwd = requestBody.get("userPwd");
        UserEntity user = userRepository.findByUserId(userId);

        if (user != null && user.getUserPwd().equals(userPwd)) {
            String token = jwtTokenProvider.createToken(userId); // JWT 토큰 생성
            return ResponseEntity.ok(token);
        } else {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("유감");
        }
    }
            // 사용자를 인증하고 세션에 사용자 정보를 저장
//            session.setAttribute("user", user);
    // http://localhost:8080/user/registerRequest
    @PostMapping("/public/user/registerRequest")
    public String registerRequest(@RequestBody UserDto userDto) {
        String userId = userDto.getUserId();
        String userPwd = userDto.getUserPwd();
        String userName = userDto.getUserName();
        String userNickname = userDto.getUserNickname();
        String userGender = userDto.getUserGender();
        String userTel = userDto.getUserTel();
        int userAge = userDto.getUserAge();

        userService.saveUser(userId, userPwd, userName, userNickname, userGender, userTel, userAge);

        return "굿";
    }

    @PostMapping("/hidden/user/registerIdCheck")
    @ResponseBody
    public ResponseEntity<Map<String, String>> registerIdCheck(@RequestBody Map<String, String> request) {
        String userId = request.get("userId");
        String message = "사용 가능한 아이디 입니다.";

        UserEntity CheckId = userRepository.findByUserId(userId);
        if (CheckId != null) {
            message = "중복된 아이디 입니다.";
        }
        Map<String, String> response = new HashMap<>();
        response.put("message", message);

        return ResponseEntity.ok(response);
    }








}


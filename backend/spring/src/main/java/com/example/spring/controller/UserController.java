package com.example.spring.controller;

import com.example.spring.dto.BoardDto;
import com.example.spring.dto.UserDto;
import com.example.spring.entity.UserEntity;
import com.example.spring.repository.UserRepository;
import com.example.spring.security.JwtAuthenticationProvider;
import com.example.spring.service.UserService;
import io.jsonwebtoken.Claims;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;
import org.hibernate.annotations.Check;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.annotation.Secured;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

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


    // http://localhost:8080/user/loginRequest
    @PostMapping("/public/user/loginRequest")
    public ResponseEntity<Map<String, Object>> loginRequest(@RequestBody Map<String, String> requestBody, HttpSession session) {
        String userId = requestBody.get("userId");
        String userPwd = requestBody.get("userPwd");
        UserEntity user = userRepository.findByUserId(userId);
        String userNickname = user.getUserNickname();
        if (user != null && user.getUserPwd().equals(userPwd)) {
            Map<String, Object> token = jwtTokenProvider.createToken(userId, userNickname); // JWT 토큰 생성
            return ResponseEntity.ok(token);
        } else {
            Map<String,Object> error = new HashMap<>();
            error.put("error" , "유감");
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(error);
        }
    }

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

    @PostMapping("/public/user/registerIdCheck")
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

    @PostMapping("/public/user/update")
    public String updateUser(
            @RequestParam("userid") String userid,
            @RequestParam("originuserPwd") String originuserPwd,
            @RequestParam("userPwd") String userPwd,
            @RequestParam("userTel") String userTel) {
        return  "두둥탁"+userService.updateUser(userid, originuserPwd, userPwd, userTel);
    }

    @PostMapping("/public/user/delete")
    public String deleteUser(@RequestParam("userid") String userid){
        return "두둥탁" + userService.deleteUser(userid);
    }

}


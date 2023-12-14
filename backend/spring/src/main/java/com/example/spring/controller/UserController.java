package com.example.spring.controller;

import com.example.spring.dto.UserDto;
import com.example.spring.entity.UserEntity;
import com.example.spring.repository.UserRepository;
import com.example.spring.service.UserService;
import jakarta.servlet.http.HttpSession;
import org.hibernate.annotations.Check;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@CrossOrigin(origins = "http://localhost:3000", methods = {RequestMethod.GET, RequestMethod.POST},  allowCredentials = "true")
// port 간 통신에서 CORS를 막기 위한 설정
@RequestMapping("/user")
public class UserController {

    private UserService userService;

    @Autowired
    private UserRepository userRepository; // 사용자 정보를 저장하는 리포지토리

    @Autowired
    public UserController(UserService userService){
        this.userService = userService;
    }

    // http://localhost:8080/user/loginRequest
    @PostMapping("/loginRequest")
    public String loginRequest(@RequestBody Map<String, String> requestBody, HttpSession session) {
        String userId = requestBody.get("userId");
        String userPwd = requestBody.get("userPwd");
        UserEntity user = userRepository.findByUserId(userId);


        if (user != null && user.getUserPwd().equals(userPwd)) {
            // 사용자를 인증하고 세션에 사용자 정보를 저장
            session.setAttribute("user", user);
            return "굿";
        } else {
            return "유감";
        }
    }

    // http://localhost:8080/user/registerRequest
    @PostMapping("/registerRequest")
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

    @PostMapping("/registerIdCheck")
    public ResponseEntity<Map<String, String>> registerIdCheck(@RequestBody Map<String, String> request) {
        String userId = request.get("userId");
        String message = "사용 가능한 아이디 입니다.";
        UserDto CheckId = userService.getUser(userId);
        if (CheckId != null) {
            message = "중복된 아이디 입니다.";
        }

        Map<String, String> response = new HashMap<>();
        response.put("message", message);

        return ResponseEntity.ok(response);
    }








}


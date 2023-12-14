package com.example.spring.controller;

import com.example.spring.dto.UserDto;
import com.example.spring.entity.UserEntity;
import com.example.spring.repository.UserRepository;
import com.example.spring.service.UserService;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

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

    // http://localhost:8080/member/loginRequest
    @PostMapping("/loginRequest")
    public String loginRequest(@RequestBody Map<String, String> requestBody, HttpSession session) {
        String userId = requestBody.get("userId");
        String userPwd = requestBody.get("userPwd");
        UserEntity user = userRepository.findByUserId(userId);


        if (user != null && user.getUserPwd().equals(userPwd)) {
            // 사용자를 인증하고 세션에 사용자 정보를 저장
            session.setAttribute("user", user);
            return "굿";
            // 메인 페이지로 리디렉션
        } else {
            return "유감"; // 인증 실패 시 로그인 페이지로 다시 이동
        }
    }

    @GetMapping("/registerRequest")
    public String handleRegisterRequest(){
//        return "redirect:http://localhost:3000/";
        return "redirect:http://localhost:8080/dd.html";
    }

    @PostMapping("/createUser")
    public UserDto createUser(@RequestBody UserDto userDto){

        String userId = userDto.getUserId();
        String userPwd = userDto.getUserPwd();
        String userName = userDto.getUserName();
        String userNickname = userDto.getUserNickname();
        String userGender = userDto.getUserGender();
        String userTel = userDto.getUserTel();
        int userAge = userDto.getUserAge();
        return null;
//        return userService.saveUser(userId, userPwd, userName, userNickname, userGender, userTel, userAge);
    }





}


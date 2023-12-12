package com.example.spring.member;

import org.springframework.web.bind.annotation.*;

@RestController
@CrossOrigin(origins = "http://localhost:3000")
public class UserController {
    @GetMapping("/loginRequest")
    public String loginRequest(@RequestBody String requestBody) {
        return requestBody;
    }

    @GetMapping("/registerRequest")
    public String handleRegisterRequest(){
//        return "redirect:http://localhost:3000/";
        return "redirect:http://localhost:8080/dd.html";
    }
    @GetMapping("/")
    public String qddq(){
        return "redirect:http://localhost:8080/dd.html";
}

}


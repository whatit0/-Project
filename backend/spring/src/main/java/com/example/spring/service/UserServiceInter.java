package com.example.spring.service;

import com.example.spring.dto.UserDto;


public interface UserServiceInter {

    UserDto saveUser(String userId, String userPwd, String userName, String userNickname, String userGender, String userTel, int userAge);

    UserDto getUser(String userId);
}

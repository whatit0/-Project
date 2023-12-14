package com.example.spring.dto;

import com.example.spring.entity.UserEntity;
import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
@ToString
@Builder
public class UserDto {

    private String userId;
    private String userName;
    private String userNickname;
    private String userPwd;
    private String userGender;
    private String userTel;
    private int userNo;
    private int userAge;

    public UserEntity toEntity(){
        return UserEntity.builder()
                .userId(userId)
                .userName(userName)
                .userNickname(userNickname)
                .userPwd(userPwd)
                .userGender(userGender)
                .userTel(userTel)
                .userAge(userAge)
                .build();
    }
}

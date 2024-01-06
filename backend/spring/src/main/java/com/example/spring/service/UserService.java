package com.example.spring.service;

import com.example.spring.dto.UserDto;
import com.example.spring.entity.UserEntity;
import com.example.spring.repository.UserRepository;
import org.slf4j.LoggerFactory;
import org.slf4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Objects;


@Service
public class UserService implements UserServiceInter {

    private final Logger logger = LoggerFactory.getLogger(UserService.class);
    private final UserRepository userRepository; // UserRepository 주입

    @Autowired
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @Override
    public UserDto saveUser(String userId, String userPwd, String userName, String userNickname, String userGender, String userTel ,int userAge) {
        logger.info("[saveUser] 유저 정보 저장");
        // UserDto 생성
        UserDto userDto = new UserDto(userId,userName, userNickname, userPwd, userGender, userTel, userAge);
        // DTO를 Entity로 변환
        UserEntity userEntity = userDto.toEntity();
        // 데이터베이스에 저장
        userEntity = userRepository.save(userEntity);
        // 저장된 Entity를 다시 DTO로 변환
        return new UserDto(
                userEntity.getUserId(),
                userEntity.getUserName(),
                userEntity.getUserNickname(),
                userEntity.getUserPwd(),
                userEntity.getUserGender(),
                userEntity.getUserTel(),
                userEntity.getUserAge()
        );
    }


    @Override
    public UserDto getUser(String userId) {
        UserEntity userEntity = userRepository.findByUserId(userId);
//        System.out.println(userEntity.getUserId());
        if (userEntity != null) {
            return new UserDto(
                    userEntity.getUserId(),
                    userEntity.getUserName(),
                    userEntity.getUserNickname(),
                    userEntity.getUserPwd(),
                    userEntity.getUserGender(),
                    userEntity.getUserTel(),
                    userEntity.getUserAge()
            );
        }
        return null;

    }

    @Override
    public String updateUser(String userId,String originuserPwd, String userPwd, String userTel) {
        UserEntity userEntity = userRepository.findByUserId(userId);

        if(!Objects.equals(userEntity.getUserPwd(), originuserPwd)) return "비밀번호가 일치하지 않습니다";

        userEntity.setUserPwd(userPwd);
        userEntity.setUserTel(userTel);
        userRepository.save(userEntity);
        return "성공";
    }

    public String deleteUser(String userId){
        UserEntity userData = userRepository.findByUserId(userId);

        // userData가 null이 아닌지 확인
        if (userData != null) {
            userRepository.deleteById(userData.getUserNo());
            return "성공";
        } else {
            return "사용자를 찾을 수 없습니다.";
        }
    }



}


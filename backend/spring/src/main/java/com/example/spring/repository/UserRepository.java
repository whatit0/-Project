package com.example.spring.repository;

import com.example.spring.entity.UserEntity;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface UserRepository extends CrudRepository<UserEntity, String> {

    UserEntity save(UserEntity userEntity);

    UserEntity findByUserId(String userId);

}

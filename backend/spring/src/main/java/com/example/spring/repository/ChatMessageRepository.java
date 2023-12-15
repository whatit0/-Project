package com.example.spring.repository;

import com.example.spring.entity.MessageEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ChatMessageRepository extends JpaRepository<MessageEntity, Integer> {
}

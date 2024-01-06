package com.example.spring.controller;

import com.example.spring.dto.ChatMessage;
import com.example.spring.repository.ChatMessageRepository;
import com.example.spring.entity.MessageEntity;
import lombok.RequiredArgsConstructor;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.simp.SimpMessageSendingOperations;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.CrossOrigin;
import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

@Controller
@CrossOrigin(origins = "http://localhost:3000")
@RequiredArgsConstructor
public class ChatController {

    private final SimpMessageSendingOperations messagingTemplate;
    private final ChatMessageRepository chatMessageRepository;

    // 접속한 유저 목록을 관리하는 Map
    private final ConcurrentHashMap<String, Set<String>> roomUserMap = new ConcurrentHashMap<>();

    @MessageMapping("/chat/message")
    public void message(ChatMessage message,  @Header("simpSessionAttributes") Map<String, Object> sessionAttributes) {
        String userId = (String) sessionAttributes.get("userId");
        message.setUserid(userId);

        // 유저의 입장 및 퇴장 처리
        if (ChatMessage.MessageType.ENTER.equals(message.getType())) {
            roomUserMap.computeIfAbsent(message.getRoomId(), k -> ConcurrentHashMap.newKeySet()).add(userId);
            message.setMessage(userId + "님이 입장하셨습니다.");
        } else if (ChatMessage.MessageType.EXIT.equals(message.getType())) {
            roomUserMap.computeIfPresent(message.getRoomId(), (k, v) -> {
                v.remove(userId);
                return v.isEmpty() ? null : v;
            });
            message.setMessage(userId + "님이 퇴장하셨습니다.");
        }
        // 채팅 메시지의 경우 데이터베이스에 저장
        else if (ChatMessage.MessageType.TALK.equals(message.getType())) {
            MessageEntity messageEntity = new MessageEntity();
            messageEntity.setContent(message.getMessage());
            Timestamp timestamp = new Timestamp(System.currentTimeMillis());
            messageEntity.setDate(timestamp);
            MessageEntity savedMessage = chatMessageRepository.save(messageEntity);

            Timestamp dbTimestamp = savedMessage.getDate();
            SimpleDateFormat dateFormat = new SimpleDateFormat("a hh:mm", Locale.KOREA);
            String formattedDate = dateFormat.format(dbTimestamp);
            message.setFormattedDate(formattedDate);
        }

        // 메시지 및 유저 목록 전송
        messagingTemplate.convertAndSend("/sub/chat/room/" + message.getRoomId(), message);
        messagingTemplate.convertAndSend("/sub/chat/room/users/" + message.getRoomId(), roomUserMap.getOrDefault(message.getRoomId(), ConcurrentHashMap.newKeySet()));
    }
}

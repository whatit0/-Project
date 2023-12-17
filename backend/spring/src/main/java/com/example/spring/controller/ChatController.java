package com.example.spring.controller;

import com.example.spring.dto.ChatMessage;
import com.example.spring.repository.ChatMessageRepository;
import com.example.spring.entity.MessageEntity;
import com.example.spring.SocketConfig.WebSockConfig;
import lombok.RequiredArgsConstructor;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.simp.SimpMessageSendingOperations;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.Locale;

@Controller
@RequiredArgsConstructor
@CrossOrigin(origins = "http://localhost:3000", methods = {RequestMethod.GET, RequestMethod.POST},  allowCredentials = "true")
@RequestMapping("/chat")
public class ChatController {

    private final SimpMessageSendingOperations messagingTemplate;
    private final ChatMessageRepository chatMessageRepository;
    private final WebSockConfig webSockConfig;

    @MessageMapping("/message")
    public void message(ChatMessage message, @Header("simpSessionId") String sessionId) {
        String userId = webSockConfig.getUserIdFromSessionId(sessionId); // 세션 ID로부터 사용자 ID 조회
        message.setUserid(userId);

        if (ChatMessage.MessageType.ENTER.equals(message.getType()) || ChatMessage.MessageType.EXIT.equals(message.getType())) {
            message.setMessage(userId + (message.getType().equals(ChatMessage.MessageType.ENTER) ? "님이 입장하셨습니다." : "님이 퇴장하셨습니다."));
        } else if (ChatMessage.MessageType.TALK.equals(message.getType())) {
            MessageEntity messageEntity = new MessageEntity();
            messageEntity.setContent(message.getMessage());
            Timestamp timestamp = new Timestamp(System.currentTimeMillis()); // 현재 시간의 타임스탬프 생성
            messageEntity.setDate(timestamp);
            MessageEntity savedMessage = chatMessageRepository.save(messageEntity);

            Timestamp dbTimestamp = savedMessage.getDate();
            SimpleDateFormat dateFormat = new SimpleDateFormat("a hh:mm", Locale.KOREA);
            String formattedDate = dateFormat.format(dbTimestamp);
            // 포맷팅된 날짜를 메시지 객체에 설정
            message.setFormattedDate(formattedDate);
        }
        messagingTemplate.convertAndSend("/sub/chat/room/" + message.getRoomId(), message);
    }
}
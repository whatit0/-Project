package com.example.spring.dto;

import lombok.Data;

@Data
public class ChatMessage {
    // 메시지 타입 : 입장, 채팅
    public enum MessageType {
        ENTER, TALK, EXIT
    }
    private MessageType type;
    private String roomId;
//    private String sender;
    private String message;
    private String userid;
    private String formattedDate;
}
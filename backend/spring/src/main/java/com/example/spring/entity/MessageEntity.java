package com.example.spring.entity;

import jakarta.persistence.*;
import lombok.Data;

import java.sql.Timestamp;

@Entity
@Data
@Table(name = "chatmessage")
public class MessageEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "chat_no")
    private int chatno;

    @Column(name = "chat_content")
    private String content;

    @Column(name = "chat_date")
    private Timestamp date;
}

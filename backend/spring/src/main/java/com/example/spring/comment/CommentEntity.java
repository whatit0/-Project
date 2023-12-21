package com.example.spring.comment;

import jakarta.persistence.*;
import lombok.Data;

import java.sql.Timestamp;

@Entity
@Data
@Table(name = "comment")
public class CommentEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "cmt_no")
    private int cmtNo;

    @Column(name = "cmt_content")
    private String cmtContent;

    @Column(name = "cmt_created")
    private Timestamp cmtCreated;

    @Column(name = "board_no")
    private int boardNo;

    @Column(name = "user_id")
    private String userId;

    public static CommentEntity toCommentEntity(CommentDto commentDto){
        CommentEntity commentEntity = new CommentEntity();
        commentEntity.setCmtNo(commentDto.getCmtNo());
        commentEntity.setCmtContent(commentDto.getCmtContent());
        commentEntity.setCmtCreated(commentDto.getCmtCreated());
        commentEntity.setBoardNo(commentDto.getBoardNo());
        commentEntity.setUserId(commentDto.getUserId());
        return commentEntity;
    }
}

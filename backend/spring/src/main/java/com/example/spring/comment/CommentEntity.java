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
    private int cmtno;

    @Column(name = "cmt_content")
    private String cmtcontent;

    @Column(name = "cmt_created")
    private Timestamp cmtcreated;

    @Column(name = "board_no")
    private int boardno;

    @Column(name = "user_id")
    private String userid;

    public static CommentEntity toCommentEntity(CommentDto commentDto){
        CommentEntity commentEntity = new CommentEntity();
        commentEntity.setCmtno(commentDto.getCmtno());
        commentEntity.setCmtcontent(commentDto.getCmtcontent());
        commentEntity.setCmtcreated(commentDto.getCmtcreated());
        commentEntity.setBoardno(commentDto.getBoardno());
        commentEntity.setUserid(commentDto.getUserid());
        return commentEntity;
    }
}

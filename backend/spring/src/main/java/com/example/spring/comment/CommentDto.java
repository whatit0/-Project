package com.example.spring.comment;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;

import java.sql.Timestamp;

@Data
@NoArgsConstructor
@AllArgsConstructor
@ToString
public class CommentDto {

    private int cmtno;
    private String cmtcontent;
    private Timestamp cmtcreated;
    private int boardno;
    private String userid;

    public static CommentDto toCommentDto(CommentEntity commentEntity){
        CommentDto commentDto = new CommentDto();
        commentDto.setCmtno(commentEntity.getCmtno());
        commentDto.setCmtcontent(commentEntity.getCmtcontent());
        commentDto.setCmtcreated(commentEntity.getCmtcreated());
        commentDto.setBoardno(commentEntity.getBoardno());
        commentDto.setUserid(commentEntity.getUserid());
        return commentDto;
    }
}

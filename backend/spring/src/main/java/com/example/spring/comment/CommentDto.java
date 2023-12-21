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

    private int cmtNo;
    private String cmtContent;
    private Timestamp cmtCreated;
    private int boardNo;
    private String userId;

    public static CommentDto toCommentDto(CommentEntity commentEntity){
        CommentDto commentDto = new CommentDto();
        commentDto.setCmtNo(commentEntity.getCmtNo());
        commentDto.setCmtContent(commentEntity.getCmtContent());
        commentDto.setCmtCreated(commentEntity.getCmtCreated());
        commentDto.setBoardNo(commentEntity.getBoardNo());
        commentDto.setUserId(commentEntity.getUserId());
        return commentDto;
    }
}

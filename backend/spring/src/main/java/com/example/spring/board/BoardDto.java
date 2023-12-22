package com.example.spring.board;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;

import java.sql.Timestamp;

@Data
@NoArgsConstructor
@AllArgsConstructor
@ToString
public class BoardDto {

    private int postno;
    private String posttitle;
    private String postcontent;
    private int postcnt;
    private String postupload;
    private Timestamp created;

    public static BoardDto toBoardDto(BoardEntity boardEntity) {
        BoardDto boardDto = new BoardDto();
        boardDto.setPostno(boardEntity.getPostno());
        boardDto.setPosttitle(boardEntity.getPosttitle());
        boardDto.setPostcontent(boardEntity.getPostcontent());
        boardDto.setPostcnt(boardEntity.getPostcnt());
        boardDto.setPostupload(boardEntity.getPostupload());
        boardDto.setCreated(boardEntity.getCreated());
        return boardDto;
    }
}

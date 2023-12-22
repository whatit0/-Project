package com.example.spring.entity;

import com.example.spring.dto.BoardDto;
import com.example.spring.service.BoardService;
import jakarta.persistence.*;
import lombok.Data;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.sql.Timestamp;

@Entity
@Data
@Table(name = "board")
@EntityListeners(AuditingEntityListener.class)
public class BoardEntity {


    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "board_no")
    private int boardno;

    @Column(name = "board_title")
    private String boardtitle;

    @Column(name = "board_content")
    private String boardcontent;

    @Column(name = "board_cnt")
    private int boardcnt;

    @Column(name = "board_filename")
    private String boardfilename;
    
    @Column(name = "board_filepath")
    private String boardfilepath;

    @CreatedDate
    @Column(name = "board_created")
    private Timestamp created;

    @Column(name = "user_id")
    private String userid;

    @CreatedDate
    @Column(name= "board_updated")
    private String updated;

    public static BoardEntity toSaveEntity(BoardDto boardDto){
        BoardEntity boardEntity = new BoardEntity();
        boardEntity.setBoardno(boardDto.getBoardno());
        boardEntity.setBoardtitle(boardDto.getBoardtitle());
        boardEntity.setBoardcontent(boardDto.getBoardcontent());
        boardEntity.setBoardcnt(boardDto.getBoardcnt());
        boardEntity.setBoardfilename(boardDto.getBoardfilename());
        boardEntity.setBoardfilepath(boardDto.getBoardfilepath());
        boardEntity.setCreated(boardDto.getCreated());
        boardEntity.setUserid(boardDto.getUserid());

        return boardEntity;
    }

    public static BoardEntity toUpdateEntity(BoardDto boardDto){
        BoardEntity boardEntity = new BoardEntity();
        boardEntity.setBoardno(boardDto.getBoardno());
        boardEntity.setBoardtitle(boardDto.getBoardtitle());
        boardEntity.setBoardcontent(boardDto.getBoardcontent());
        boardEntity.setBoardcnt(boardDto.getBoardcnt());
        boardEntity.setBoardfilename(boardDto.getBoardfilename());
        boardEntity.setBoardfilepath(boardDto.getBoardfilepath());
        boardEntity.setCreated(boardDto.getCreated());
        boardEntity.setUserid(boardDto.getUserid());
        return boardEntity;
    }
}
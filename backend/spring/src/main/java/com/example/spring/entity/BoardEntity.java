package com.example.spring.entity;

import java.sql.Timestamp;

import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import com.example.spring.dto.BoardDto;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EntityListeners;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Data;

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
    private Timestamp updated;

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
        boardEntity.setUpdated(boardDto.getUpdated());
        boardEntity.setUserid(boardDto.getUserid());
        return boardEntity;
    }
}
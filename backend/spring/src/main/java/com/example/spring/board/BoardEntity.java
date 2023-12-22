package com.example.spring.board;

import jakarta.persistence.*;
import lombok.Data;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.sql.Timestamp;

@Entity
@Data
@Table(name = "post")
@EntityListeners(AuditingEntityListener.class)
public class BoardEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "post_no")
    private int postno;

    @Column(name = "post_title")
    private String posttitle;

    @Column(name = "post_content")
    private String postcontent;

    @Column(name = "post_cnt")
    private int postcnt;

    @Column(name = "post_upload")
    private String postupload;

    @CreatedDate
    @Column(name = "post_created")
    private Timestamp created;

//    @Column(name = "user_no")
//    private int userno;

    public static BoardEntity toSaveEntity(BoardDto boardDto){
        BoardEntity boardEntity = new BoardEntity();
        boardEntity.setPostno(boardDto.getPostno());
        boardEntity.setPosttitle(boardDto.getPosttitle());
        boardEntity.setPostcontent(boardDto.getPostcontent());
        boardEntity.setPostcnt(boardDto.getPostcnt());
        boardEntity.setPostupload(boardDto.getPostupload());
        boardEntity.setCreated(boardDto.getCreated());
        return boardEntity;
    }
}

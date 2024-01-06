package com.example.spring.comment;

import com.example.spring.dto.BoardDto;
import com.example.spring.entity.BoardEntity;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
@RequiredArgsConstructor
public class CommentService {

    private final CommentRepository commentRepository;

    // 댓글 저장
    public void commentSave(CommentDto commentDto){
        CommentEntity commentEntity = CommentEntity.toCommentEntity(commentDto);
        commentRepository.save(commentEntity);
    }

    // 게시글 번호에 따른 댓글 검색
    public List<CommentDto> commentList(int boardno){
        List<CommentEntity> commentEntityList = commentRepository.findByBoardno(boardno);
        List<CommentDto> commentDtos = new ArrayList<>();
        for (CommentEntity commentEntity : commentEntityList){
            CommentDto commentDto = CommentDto.toCommentDto(commentEntity);
            commentDtos.add(commentDto);
        }
        return commentDtos;
    }

    // 본인 댓글 조
    public List<CommentDto> commentFindUserid(String userid){
        List<CommentEntity> commentEntityList = commentRepository.findByUserid(userid);
        List<CommentDto> commentDtos = new ArrayList<>();
        for (CommentEntity commentEntity : commentEntityList) {
            CommentDto commentDto = CommentDto.toCommentDto(commentEntity);
            commentDtos.add(commentDto);
        }
        return commentDtos;
    }

    public void commentUpdate(int boardno, String cmtcontent){
        commentRepository.update(boardno, cmtcontent);
    }

    public void comentDelete(int cmtno) {
        commentRepository.deleteById(cmtno);
    }

}

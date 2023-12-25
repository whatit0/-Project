package com.example.spring.service;

import com.example.spring.dto.BoardDto;
import com.example.spring.entity.BoardEntity;
import com.example.spring.repository.BoardRepository;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class BoardService {

    private final BoardRepository boardRepository;

    // 게시글 저장
    public void boardInfoInsertSave(BoardDto boardDto){
        BoardEntity boardEntity = BoardEntity.toSaveEntity(boardDto);
        boardRepository.save(boardEntity);
    }

    // 게시글 목록 보기
    public List<BoardDto> boardListAll() {
        List<BoardEntity> boardEntityList = boardRepository.findAll();
        List<BoardDto> boardDtoList = new ArrayList<>();
        for (BoardEntity boardEntity: boardEntityList) {
            boardDtoList.add(BoardDto.toBoardDto(boardEntity));
        }
        return boardDtoList;
    }

    // 게시글 조회수 증가
    @Transactional
    public void boardUpdateHit(int boardno) {
        boardRepository.updateHit(boardno);
    }
    public void boardUpdate(BoardDto boardDto) {
        BoardEntity boardEntity = BoardEntity.toUpdateEntity(boardDto);
        boardRepository.save(boardEntity);
    }

    public void boardUpdatefile(BoardDto boardDto) {
        BoardEntity boardEntity = BoardEntity.toUpdateEntity(boardDto);
        boardRepository.save(boardEntity);
    }

    // 게시글 상세 보기
    public BoardDto boardFindId(int boardno) {
        Optional<BoardEntity> optionalBoardEntity = boardRepository.findById(boardno);
        if(optionalBoardEntity.isPresent()) {
            BoardEntity boardEntity = optionalBoardEntity.get();
            BoardDto boardDto = BoardDto.toBoardDto(boardEntity);
            return boardDto;
        } else {
            return null;
        }

    }
    public void boardDelete(int boardno) {
        boardRepository.deleteById(boardno);
    }

    // 작성자로 게시글 검색
    public List<BoardDto> boardFindWriter(String writer) {
        List<BoardEntity> boardEntities = boardRepository.findByWriter(writer);
        List<BoardDto> boardDtos = new ArrayList<>();
        for (BoardEntity boardEntity : boardEntities) {
            BoardDto boardDto = BoardDto.toBoardDto(boardEntity);
            boardDtos.add(boardDto);
        }
        return boardDtos;
    }

    // 제목으로 게시글 검회
    public List<BoardDto> boardFindTitle(String title) {
        List<BoardEntity> boardEntities = boardRepository.findByTitle(title);
        List<BoardDto> boardDtos = new ArrayList<>();
        for (BoardEntity boardEntity : boardEntities) {
            BoardDto boardDto = BoardDto.toBoardDto(boardEntity);
            boardDtos.add(boardDto);
        }
        return boardDtos;
    }


    // 본인 게시글 조회

    public List<BoardDto> boardFindUserid(String userid) {
        List<BoardEntity> boardEntities = boardRepository.findByUserid(userid);
        List<BoardDto> boardDtos = new ArrayList<>();
        for (BoardEntity boardEntity : boardEntities) {
            BoardDto boardDto = BoardDto.toBoardDto(boardEntity);
            boardDtos.add(boardDto);
        }
        return boardDtos;
    }


}
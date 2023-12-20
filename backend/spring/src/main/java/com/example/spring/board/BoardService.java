package com.example.spring.board;

import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
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

//    public BoardDto boardUpdate(BoardDto boardDto) {
//        BoardEntity boardEntity = BoardEntity.toUpdateEntity(boardDto);
//        boardRepository.save(boardEntity);
//        return boardFindId(boardDto.getId());
//    }

    public void boardDelete(int boardno) {
        boardRepository.deleteById(boardno);
    }


}
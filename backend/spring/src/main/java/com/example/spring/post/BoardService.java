package com.example.spring.post;

import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

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
    public void boardUpdateHit(int postno) {
        boardRepository.updateHit(postno);
    }

    // 게시글 상세 보기
    public BoardDto boardFindId(int postno) {
        Optional<BoardEntity> optionalBoardEntity = boardRepository.findById(postno);
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

    public void boardDelete(int postno) {
        boardRepository.deleteById(postno);
    }


}

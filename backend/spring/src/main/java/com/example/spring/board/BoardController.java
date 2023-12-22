package com.example.spring.board;

import lombok.RequiredArgsConstructor;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

//@Controller
@RestController
@RequiredArgsConstructor
@CrossOrigin(origins = "http://localhost:3000", methods = {RequestMethod.GET, RequestMethod.POST},  allowCredentials = "true")
@RequestMapping("/board")
public class BoardController {


    @GetMapping("/test")
    public List<BoardDto> test(){
        return boardService.boardListAll();
    }


    private final BoardService boardService;

    @GetMapping("/list")
    public String boardList(Model model){
        List<BoardDto> boardDtoList = boardService.boardListAll();
        model.addAttribute("boardList", boardDtoList);
        return "board/PostList";
    }

    // 게시글 작성 페이지 이동
    @GetMapping("/write")
    public String PostWrite(){
        return "PostWrite";
    }

    @PostMapping("/write")
    public String PostWriteto(BoardDto boardDto){
        boardService.boardInfoInsertSave(boardDto);
        return "redirect:/board/list";
    }


}

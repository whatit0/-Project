package com.example.spring.post;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
//@RestController
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
        return "boardList";
    }

    // 게시글 작성 페이지 이동
    @GetMapping("/write")
    public String PostWrite(){
        return "boardWrite";
    }

    // 게시글 작성 후 목록 반환
    @PostMapping("/write")
    public String PostWriteto(BoardDto boardDto){
        boardService.boardInfoInsertSave(boardDto);
        return "redirect:/board/list";
    }

    // 게시글 상세 보기 페이지
    @GetMapping("/detail/{postno}")
    public String BoardDetail(@PathVariable int postno, Model model) {
        boardService.boardUpdateHit(postno);
        BoardDto boardDto = boardService.boardFindId(postno);
        model.addAttribute("board", boardDto);
        return "boardDetail";
    }

    @GetMapping("/delete/{postno}")
    public String BoardDeleteForm(@PathVariable int postno) {
        boardService.boardDelete(postno);
        return "redirect:/board/list";
    }
}
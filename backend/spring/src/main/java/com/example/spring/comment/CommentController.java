package com.example.spring.comment;

import com.example.spring.dto.BoardDto;
import com.example.spring.security.JwtAuthenticationProvider;
import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.parameters.P;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;

@RestController
@RequiredArgsConstructor
@CrossOrigin(origins = "http://localhost:3000", methods = {RequestMethod.GET, RequestMethod.POST},  allowCredentials = "true")
@RequestMapping("/public/comment")
public class CommentController {

    private final CommentService commentService;
    private final JwtAuthenticationProvider jwtTokenProvider;

    @PostMapping("/write")
    public String commentWrite(
            @RequestParam("boardno") int boardno,
            @RequestParam("cmtcontent") String cmtcontent,
            HttpServletRequest request
            ) {
        String accessToken = request.getHeader("Authorization");
        if (accessToken != null && accessToken.startsWith("Bearer ")) {
            accessToken = accessToken.substring(7);
        }

        Authentication authentication = jwtTokenProvider.getAuthentication(accessToken);
        String userId = (String) authentication.getPrincipal();
        CommentDto commentDto = new CommentDto();
        commentDto.setUserid(userId);
        commentDto.setBoardno(boardno);
        commentDto.setCmtcontent(cmtcontent);
        commentService.commentSave(commentDto);
        return "두둥탁";
    }

    // 게시글 번호에 따른 댓글 조회
    @PostMapping("/list")
    public List<CommentDto> commentDtoList(@RequestParam("boardno") int boardno){
        List<CommentDto> commentDtoList = new ArrayList<>();
        commentDtoList = commentService.commentList(boardno);
        return commentDtoList;
    }

    @PostMapping("/mycommentlist")
    public List<CommentDto> commentSearch(@RequestParam("userid") String userId) {
        List<CommentDto> commentDtos = commentService.commentFindUserid(userId);
        return commentDtos;}


    @PostMapping("/update")
    public String commentUpdate(
            @RequestParam("boardno") int boardno,
            @RequestParam("cmtcontent") String cmtcontent){
        commentService.commentUpdate(boardno, cmtcontent);
        return "두둥탁";
    }

    @PostMapping("/delete")
    public String CommentDelete(@RequestParam("cmtno") int cmtno){
        commentService.comentDelete(cmtno);
        return "두둥탁";
    }


}

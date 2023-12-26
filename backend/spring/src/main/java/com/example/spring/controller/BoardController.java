package com.example.spring.controller;

import com.example.spring.dto.BoardDto;
import com.example.spring.service.BoardService;
import com.example.spring.repository.UserRepository;
import com.example.spring.security.JwtAuthenticationProvider;
import com.example.spring.service.UserService;
import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.PropertySource;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;


//@Controller
@RestController
@RequiredArgsConstructor
@CrossOrigin(origins = "http://localhost:3000", methods = {RequestMethod.GET, RequestMethod.POST},  allowCredentials = "true")
@RequestMapping("/public/board")
@PropertySource("classpath:application.properties")
public class BoardController {

    private final UserService userService;
    private final JwtAuthenticationProvider jwtTokenProvider;
    private final UserRepository userRepository;
    private final BoardService boardService;
    @Value("${FILE_LOCAL_DIRECTORY}")
    private String filedir;

    @GetMapping("/test")
    public List<BoardDto> test() {
        return boardService.boardListAll();
    }

    // 게시글 작성 페이지 이동
    @GetMapping("/write")
    public String PostWrite() {
        return "boardWrite";
    }

    // 게시글 작성 후 목록 반환
    @PostMapping("/write")
    public String postWrite(
            @RequestParam("boardtitle") String boardtitle,
            @RequestParam("boardcontent") String boardcontent,
            @RequestParam(value = "boardFilename", required = false) MultipartFile boardFilename,
            HttpServletRequest request
    ) {
        String accessToken = request.getHeader("Authorization");
        if (accessToken != null && accessToken.startsWith("Bearer ")) {
            accessToken = accessToken.substring(7);
        }

        Authentication authentication = jwtTokenProvider.getAuthentication(accessToken);
        String userId = (String) authentication.getPrincipal();
        BoardDto boardDto = new BoardDto();
        boardDto.setUserid(userId);
        boardDto.setBoardtitle(boardtitle);
        boardDto.setBoardcontent(boardcontent);

        // 파일 처리
        if (boardFilename != null && !boardFilename.isEmpty()) {
            String originalFilename = boardFilename.getOriginalFilename();
            String fileExtension = originalFilename.substring(originalFilename.lastIndexOf("."));
            String randomFileName = UUID.randomUUID() + fileExtension;
            String filepath = filedir + randomFileName;

            // 파일 시스템에 파일 저장
            try {
                Path path = Paths.get(filepath);
                Files.copy(boardFilename.getInputStream(), path, StandardCopyOption.REPLACE_EXISTING);
                boardDto.setBoardfilename(randomFileName); // 난수로 생성한 파일 이름 설정
                boardDto.setBoardfilepath(filepath);
            } catch (IOException e) {
                e.printStackTrace();
                return "파일 업로드 실패";
            }
        }

        boardService.boardInfoInsertSave(boardDto);
        return "두둥탁";
    }



    // 게시글 상세 보기 페이지
    @GetMapping("/detail/{boardno}")
    public ResponseEntity<?> BoardDetail(@PathVariable int boardno) {

        boardService.boardUpdateHit(boardno);
        BoardDto boardDto = boardService.boardFindId(boardno);

            Map<String, Object> responseData = new HashMap<>();
            responseData.put("boardData", boardDto);
            if (boardDto != null) {
            return ResponseEntity.ok(responseData);
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    @GetMapping("/detail/token/{boardno}")
    public ResponseEntity<?> BoardToeknDetail(@PathVariable int boardno, HttpServletRequest request) {

        String accessToken = request.getHeader("Authorization");
        if (accessToken != null && accessToken.startsWith("Bearer ")) {
            accessToken = accessToken.substring(7);
        }
        Authentication authentication = jwtTokenProvider.getAuthentication(accessToken);
        String userId = (String) authentication.getPrincipal();
        boardService.boardUpdateHit(boardno);
        BoardDto boardDto = boardService.boardFindId(boardno);
        String boardid = boardDto.getUserid();
        // 게시글 작성자와 현재 사용자가 같은지 확인
        boolean isOwner = boardid.equals(userId);
        // 응답 데이터 구성
        Map<String, Object> responseData = new HashMap<>();
        responseData.put("boardData", boardDto);
        responseData.put("isOwner", isOwner);
        if (boardDto != null) {
            return ResponseEntity.ok(responseData);
        } else {
            return ResponseEntity.notFound().build();
        }
    }


    @GetMapping("/update")
    public ResponseEntity<BoardDto> BoardUpdate(){

        return null;
    }


    @GetMapping("/delete")
    public String BoardDeleteForm(@RequestParam int boardno) {
        System.out.println(boardno);
        boardService.boardDelete(boardno);
        return "두둥탁";
    }
}

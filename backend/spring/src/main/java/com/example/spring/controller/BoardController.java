package com.example.spring.controller;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.PropertySource;
import org.springframework.data.domain.Sort;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import com.example.spring.dto.BoardDto;
import com.example.spring.entity.BoardEntity;
import com.example.spring.repository.BoardRepository;
import com.example.spring.repository.UserRepository;
import com.example.spring.security.JwtAuthenticationProvider;
import com.example.spring.service.BoardService;
import com.example.spring.service.UserService;

import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;


//@Controller
@RestController
@RequiredArgsConstructor
@PropertySource("classpath:application.properties")
@CrossOrigin(origins = "http://localhost:3000", methods = {RequestMethod.GET, RequestMethod.POST},  allowCredentials = "true")
@RequestMapping("/public/board")
public class BoardController {

    @Value("${FILE_LOCAL_DIRECTORY}")
    private String filedir;

    private final UserService userService;
    private final JwtAuthenticationProvider jwtTokenProvider;
    private final UserRepository userRepository;
    private final BoardService boardService;
    private final BoardRepository boardRepository;


    @GetMapping("/test")
    public List<BoardEntity> test() {
        return boardRepository.findAll(Sort.by(Sort.Direction.DESC, "boardno"));
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

    @PostMapping("/search")
    public List<BoardDto> BoardSearch(
            @RequestParam("type") String type,
            @RequestParam("title") String title) {
        List<BoardDto> boardDtos = new ArrayList<>();

        if (type.equals("writer")) {
            boardDtos = boardService.boardFindWriter(title);
        } else {
            boardDtos = boardService.boardFindTitle(title);
        }
        System.out.println("\n\n\n\n\n\n\n\n");
        System.out.println(boardDtos+"\n\n\n\n\n\n\n\n");
        return boardDtos;
    }

    @PostMapping("/update")
    public String BoardUpdate(
            @RequestParam("boardtitle") String boardtitle,
            @RequestParam("boardcontent") String boardcontent,
            @RequestParam("boardno") int boardno,
            @RequestParam(value = "boardFilename", required = false) MultipartFile boardFilename) {
        BoardDto boardDto = boardService.boardFindId(boardno);
        boardDto.setBoardtitle(boardtitle);
        boardDto.setBoardcontent(boardcontent);
        if (boardFilename != null) {
            String originalFilename = boardFilename.getOriginalFilename();
            String fileExtension = originalFilename.substring(originalFilename.lastIndexOf("."));
            String randomFileName = UUID.randomUUID() + fileExtension;
            String filepath = filedir + randomFileName;
            try {
                Path path = Paths.get(filepath);
                Files.copy(boardFilename.getInputStream(), path, StandardCopyOption.REPLACE_EXISTING);
                boardDto.setBoardfilename(randomFileName); // 난수로 생성한 파일 이름 설정
                boardDto.setBoardfilepath(filepath);
            } catch (IOException e) {
                e.printStackTrace();
                return "파일 업로드 실패";
            }
            boardService.boardUpdatefile(boardDto);
            return "두둥탁 이미지 저장 완료";

        }
            boardService.boardUpdate(boardDto);
        return "두둥탁 이미지 저장 안함";
    }

    @GetMapping("/delete")
    public String BoardDeleteForm(@RequestParam int boardno) {
        System.out.println(boardno);
        boardService.boardDelete(boardno);
        return "두둥탁";
    }
}

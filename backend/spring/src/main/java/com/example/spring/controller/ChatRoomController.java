package com.example.spring.controller;

import com.example.spring.dto.ChatRoom;
import com.example.spring.repository.ChatRoomRepository;
import jakarta.servlet.http.HttpSession;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RequiredArgsConstructor
@Controller
@CrossOrigin(origins = "http://localhost:3000", methods = {RequestMethod.GET, RequestMethod.POST},  allowCredentials = "true")
@RequestMapping("/chat")
public class ChatRoomController {

    private final ChatRoomRepository chatRoomRepository;


    @GetMapping("/rooms")
    @ResponseBody
    public List<ChatRoom> room() {
        return chatRoomRepository.findAllRoom();
    }

    @PostMapping("/room")
    @ResponseBody
    public ChatRoom createRoom(@RequestParam String name) {
        return chatRoomRepository.createChatRoom(name);
    }

    @GetMapping("/room/enter/{roomId}")
    @ResponseBody
    public ResponseEntity<?> roomDetail(@PathVariable String roomId, HttpSession session) {
        ChatRoom room = chatRoomRepository.findRoomById(roomId);
        if (room != null) {
            String userId = (String) session.getAttribute("userId");
            // 필요한 데이터를 Map이나 DTO에 담아 반환
            Map<String, Object> response = new HashMap<>();
            response.put("roomId", roomId);
            response.put("userId", userId);
            response.put("room", room);
            return ResponseEntity.ok(response);
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    @GetMapping("/room/{roomId}")
    @ResponseBody
    public ChatRoom roomInfo(@PathVariable String roomId) {
        return chatRoomRepository.findRoomById(roomId);
    }
}
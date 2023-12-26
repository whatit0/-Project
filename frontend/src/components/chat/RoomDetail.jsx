import axios from 'axios';
import React, { useEffect, useRef, useState } from 'react';
import SockJS from 'sockjs-client';
import Stomp from 'stompjs';
import '../style/bootstrap.css';
import '../style/room.css';

const RoomDetail = ({ roomId }) => {
    const [room, setRoom] = useState({});
    const [name, setName] = useState('');
    const [userId, setUserId] = useState('');
    const [message, setMessage] = useState('');
    const [messages, setMessages] = useState([]);
    const [connected, setConnected] = useState(false);
    const stompClient = useRef(null);
    const [Id, setId] = useState('');
    const [activeUsers, setActiveUsers] = useState([]);

    useEffect(() => {
        // Room 정보 가져오기
        axios.get(`http://localhost:8080/chat/room/${roomId}`)
            .then(response => {
                if (response.data) {
                    setRoom(response.data);
                    setName(response.data.name);
                    setUserId(response.data.userId);
                } else {
                    setName(localStorage.getItem('wschat.roomName'));
                }
            })
            .catch(error => {
                console.error(error);
                setName(localStorage.getItem('wschat.roomName'));
            });

        // WebSocket 설정
        const token = localStorage.getItem('accessToken');
        // 토큰 디코딩 및 유저 아이디 추출
        const tokenData = token.split('.')[1]; // JWT 토큰의 두 번째 부분 선택
        const decodedTokenData = JSON.parse(atob(tokenData)); // Base64 디코딩 및 JSON 파싱
        const userId = decodedTokenData.Id; // 토큰에서 유저 아이디 추출
        setId(userId);

        const encodedToken = encodeURIComponent(token); // 토큰을 URL 인코딩
        const socket = new SockJS(`http://localhost:8080/ws-stomp?access_token=${encodedToken}`);

        stompClient.current = Stomp.over(socket);
        stompClient.current.connect({}, (frame) => {
            setConnected(true);
            subscribeToRoom(roomId);

            if (stompClient.current && stompClient.current.connected) {
                const enterMessage = {
                    type: 'ENTER',
                    roomId: roomId,
                    userid: userId,
                };
                stompClient.current.send("/pub/chat/message", {}, JSON.stringify(enterMessage));
            }
        }, (error) => {
            alert("WebSocket 연결 에러: " + error);
        });

        // 컴포넌트 언마운트 시 WebSocket 연결 종료
        return () => {
            if (stompClient.current && stompClient.current.connected) {
                stompClient.current.disconnect();
            }
        };
    }, [roomId]); // roomId가 변경될 때마다 실행

    // 채팅방 구독 로직
    const subscribeToRoom = () => {
        if (stompClient.current && stompClient.current.connected) {
            // 채팅 메시지 구독
            stompClient.current.subscribe(`/sub/chat/room/${roomId}`, (message) => {
                const recv = JSON.parse(message.body);
                // 메시지 업데이트
                setMessages(prevMessages => [...prevMessages, {
                    userid: recv.userid,
                    message: recv.message,
                    formattedDate: recv.formattedDate
                }]);
            });

            // 유저 목록 구독
            stompClient.current.subscribe(`/sub/chat/room/users/${roomId}`, (message) => {
                const users = JSON.parse(message.body);
                // 유저 목록 업데이트
                setActiveUsers(users);
            });
        }
    };

    const sendMessage = () => {
        const messageContent = message.trim();
        if (messageContent && stompClient.current.connected) {
            const chatMessage = {
                type: 'TALK',
                roomId,
                userid: userId,
                message: messageContent,
            };
            stompClient.current.send("/pub/chat/message", {}, JSON.stringify(chatMessage));
            setMessage('');
        } else {
            console.log("메시지를 보낼 수 없습니다.");
        }
    };

    const leaveRoom = () => {
        if (stompClient.current && stompClient.current.connected) {
            stompClient.current.send("/pub/chat/message", {}, JSON.stringify({ type: 'EXIT', roomId, userid: userId }));
            window.location.href = '/chatList';
        } else {
            console.error("웹소켓 연결이 끊어진 상태입니다.");
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    };

    // 메시지 목록 스크롤
    useEffect(() => {
        const scrollToEnd = () => {
            const container = document.querySelector(".chatbox__messages__box");
            if (container) {
                container.scrollTop = container.scrollHeight;
            }
        };
        scrollToEnd();
    }, [messages]);


    return (
        <div className='chat_detail_con'>
            <div className="chat-header">
                <h1>채팅 방: {name}</h1>
                <div className="buttons">
                    <button className="btn-hover color-11" onClick={leaveRoom}>퇴장</button>
                </div>
            </div>
            <div className='chatbox'>
                <div className="chatbox__user-list">
                    <h1>접속 유저</h1>
                    {activeUsers.map((user, index) => (
                        <div key={index} className='chatbox__user--active'>
                            <p className="user">{user}</p>
                        </div>
                    ))}
                </div>
                <div className="chatbox__messages">
                    <div className='chatbox__messages__box'>
                        {messages.map((msg, index) => {
                            const isOwnMessage = msg.userid === Id; // 현재 사용자의 메시지인지 확인
                            return (
                                <div key={index} className={`chatbox_user_message ${isOwnMessage ? 'own-message' : ''}`}>
                                    <div>
                                        <div className='ind-message-top flex'>
                                            <p className="name">{msg.userid}</p>
                                            <p className="date">{msg.formattedDate}</p>
                                        </div>
                                        <div className="ind-message">
                                            <p className="message">{msg.message}</p>
                                        </div>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                    <div className="send_form_con flex">
                        <input
                            type="text"
                            className="send_input"
                            value={message}
                            onChange={(e) => setMessage(e.target.value)}
                            placeholder="메시지를 입력하세요"
                            onKeyDown={handleKeyDown} // 엔터 키 이벤트 핸들러 추가
                        />
                        <div className="buttons">
                            <button className="" onClick={sendMessage}>
                                <span className="material-symbols-rounded white fs30 fw400">near_me</span>
                            </button>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    );
};

export default RoomDetail;
import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import Stomp from 'stompjs';
import SockJS from 'sockjs-client';
// import styles from "../style/room.css";
import '../style/room.css'
import '../style/bootstrap.css'

const RoomDetail = () => {
    const [room, setRoom] = useState({});
    const [name, setName] = useState('');
    const [userId, setUserId] = useState('');
    const [message, setMessage] = useState('');
    const [messages, setMessages] = useState([]);
    const roomId = localStorage.getItem('wschat.roomId');
    const [connected, setConnected] = useState(false); // 연결 상태 추적
    const stompClient = useRef(null);


    useEffect(() => {
        // Room 정보 가져오기
        axios.get('http://localhost:8080/chat/room/' + roomId)
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
        const socket = new SockJS('http://localhost:8080/ws-stomp');
        stompClient.current = Stomp.over(socket);

        stompClient.current.connect({}, (frame) => { // .current를 통해 접근
            // 연결 성공 시
            setConnected(true);
            subscribeToRoom();

            if (stompClient.current && stompClient.current.connected) {
                const enterMessage = {
                    type: 'ENTER',
                    roomId: roomId,
                    userid: userId,
                    message: `${userId} has entered the room.`
                };
                stompClient.current.send("/pub/chat/message", {}, JSON.stringify(enterMessage));
            }
        }, (error) => {
            alert("WebSocket 연결 에러 : " + error);
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
            stompClient.current.subscribe(`/sub/chat/room/${roomId}`, (message) => {
                const recv = JSON.parse(message.body);
                setMessages(prevMessages => [...prevMessages, {
                    userid: recv.userId,
                    message: recv.message,
                    formattedDate: recv.formattedDate
                }]);
            });
        }
    }

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
            stompClient.current.send("/pub/chat/message", {}, JSON.stringify({type:'EXIT', roomId, userid: userId}));
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
    const scrollToEnd = () => {
        const container = document.querySelector(".chatbox__messages");
        if (container) {
            container.scrollTop = container.scrollHeight;
        }
    };

    useEffect(() => {
        scrollToEnd();
    }, [messages]);


    return (
        <div className='container'>
            <div className="chat-header">
                <h1>채팅 방 : {name}</h1>
                <div className="buttons">
                    <button className="btn-hover color-11" onClick={leaveRoom}>퇴장</button>
                </div>
            </div>
            <div className='chatbox'>
                <div className="chatbox__user-list">
                    <h1>접속 유저</h1>
                    <div className='chatbox__user--active'>
                        <p>{userId}</p>
                    </div>
                </div>
                <div className="chatbox__messages">
                    {messages.map((msg, index) => {
                        return (
                            <div key={index} className="chatbox__messages__user-message">
                                <div className="chatbox__messages__user-message--ind-message">
                                    <p className="name">{msg.userid}</p>
                                    <p className="message">{msg.message}</p>
                                </div>
                                <p className="date">{msg.formattedDate}</p>
                            </div>
                        );
                    })}
                </div>
                <div className="input-group">
                    <input
                        type="text"
                        className="form-control"
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        placeholder="메시지를 입력하세요"
                        onKeyDown={handleKeyDown} // 엔터 키 이벤트 핸들러 추가
                    />
                    <div className="buttons">
                        <button className="btn-hover color-1" onClick={sendMessage}>전송</button>
                    </div>
                </div>
            </div>
        </div>
    );
};
export default RoomDetail;
import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import Stomp from 'stompjs';
import SockJS from 'sockjs-client';

const RoomDetail = ({ match }) => {
    const roomId = match.params.roomId;
    const [roomName, setRoomName] = useState('');
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');
    const userId = localStorage.getItem('userId');

    // stompClient를 useRef로 저장
    const stompClient = useRef(null);

    useEffect(() => {
        fetchRoomDetails();
        setupWebSocket();
        // useEffect 청소 함수
        return () => {
            if (stompClient.current) {
                stompClient.current.disconnect();
            }
        };
    }, [fetchRoomDetails, setupWebSocket]); // 의존성 배열에 함수 추가

    const fetchRoomDetails = async () => {
        // ... 기존 코드
    };

    const setupWebSocket = () => {
        const socket = new SockJS('http://localhost:8080/ws-stomp');
        stompClient.current = Stomp.client(socket);

        stompClient.current.connect({}, () => {
            stompClient.current.subscribe(`http://localhost:8080/sub/chat/room/${roomId}`, (message) => {
                const newMessage = JSON.parse(message.body);
                setMessages(prevMessages => [...prevMessages, newMessage]);
            });
        });
    };

    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!newMessage.trim()) return;
        const message = { type: 'TALK', roomId, userid: userId, message: newMessage };
        stompClient.current.send("http://localhost:8080/pub/chat/message", {}, JSON.stringify(message));
        setNewMessage('');
    };

    return (
        <div className='container'>
            <div className="chat-header">
                <h1>{roomName}</h1>
                <button className="btn btn-danger" onClick={() => window.location.href = 'http://localhost:8080/chat/room'}>퇴장</button>
            </div>
            <div className='chatbox'>
                <div className="chatbox__messages">
                    {messages.map((msg, index) => (
                        <div key={index} className="chatbox__messages__user-message">
                            <div className="chatbox__messages__user-message--ind-message">
                                <p className="name">{msg.userid}</p>
                                <p className="message">{msg.message}</p>
                                <p className="date">{msg.formattedDate}</p>
                            </div>
                        </div>
                    ))}
                </div>
                <form className="input-group" onSubmit={handleSendMessage}>
                    <input
                        type="text"
                        className="form-control"
                        value={newMessage}
                        onChange={(e) => setNewMessage(e.target.value)}
                        placeholder="메시지를 입력하세요"
                    />
                    <div className="input-group-append">
                        <button className="btn btn-primary" type="submit">전송</button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default RoomDetail;

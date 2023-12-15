import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Stomp from 'stompjs';
import SockJS from 'sockjs-client';

const RoomDetail = ({ match }) => {
    const roomId = match.params.roomId;
    const [roomName, setRoomName] = useState('');
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');
    const userId = localStorage.getItem('userId');

    useEffect(() => {
        fetchRoomDetails();
        setupWebSocket();
    }, []);

    const fetchRoomDetails = async () => {
        try {
            const response = await axios.get(`/chat/room/${roomId}`);
            setRoomName(response.data.name);
        } catch (error) {
            console.error('Error fetching room details:', error);
        }
    };

    const setupWebSocket = () => {
        const socket = new SockJS('/ws-stomp');
        const stompClient = Stomp.over(socket);

        stompClient.connect({}, () => {
            stompClient.subscribe(`/sub/chat/room/${roomId}`, (message) => {
                const newMessage = JSON.parse(message.body);
                setMessages(prevMessages => [...prevMessages, newMessage]);
            });
        });

        // Cleanup on unmount
        return () => {
            stompClient.disconnect();
        };
    };

    const handleSendMessage = async () => {
        if (!newMessage.trim()) return;
        const message = { type: 'TALK', roomId, userid: userId, message: newMessage };
        stompClient.send("/pub/chat/message", {}, JSON.stringify(message));
        setNewMessage('');
    };

    return (
        <div className='container'>
            <div className="chat-header">
                <h1>{roomName}</h1>
                <button className="btn btn-danger" onClick={() => window.location.href = '/chat/room'}>퇴장</button>
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

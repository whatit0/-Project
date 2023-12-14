import React, { useEffect, useState } from 'react';
import axios from 'axios';

const RoomList = () => {
    const [rooms, setRooms] = useState([]);
    const [newRoomName, setNewRoomName] = useState('');

    useEffect(() => {
        fetchChatRooms();
    }, []);

    const fetchChatRooms = async () => {
        try {
            const response = await axios.get('/chat/rooms');
            setRooms(response.data);
        } catch (error) {
            console.error('Error fetching chat rooms:', error);
        }
    };

    const handleCreateRoom = async () => {
        if (newRoomName.trim() === '') return;
        try {
            const response = await axios.post('/chat/room', { name: newRoomName });
            localStorage.setItem('wschat.roomId', response.data.roomId);
            localStorage.setItem('wschat.roomName', response.data.name);
            window.location.href = `/chat/room/enter/${response.data.roomId}`;
        } catch (error) {
            console.error('Error creating chat room:', error);
        }
    };

    return (
        <div className="container mt-5">
            <h2>채팅방 목록</h2>
            <div className="input-group mt-3">
                <input
                    type="text"
                    className="form-control"
                    placeholder="채팅방 이름 입력"
                    value={newRoomName}
                    onChange={(e) => setNewRoomName(e.target.value)}
                />
                <div className="input-group-append">
                    <button className="btn btn-primary" onClick={handleCreateRoom}>방 생성</button>
                </div>
            </div>
            <ul className="list-group mt-3">
                {rooms.map(room => (
                    <li
                        key={room.roomId}
                        className="list-group-item"
                        onClick={() => window.location.href = `/chat/room/enter/${room.roomId}`}
                    >
                        {room.name}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default RoomList;

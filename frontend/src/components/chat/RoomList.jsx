import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // useNavigate 훅 임포트
import '../style/bootstrap.css'


const RoomList = () => {
    const [rooms, setRooms] = useState([]);
    const [newRoomName, setNewRoomName] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        fetchChatRooms();
    }, []);

    const fetchChatRooms = async () => {
        try {
            const response = await axios.get('http://localhost:8080/chat/rooms');
            setRooms(response.data);
        } catch (error) {
            console.error('Error fetching chat rooms:', error);
        }
    };

    const handleCreateRoom = (e) => {
        e.preventDefault();
        createRoom();
    };

    const createRoom = async () => {
        if (newRoomName.trim() === '') return;
        try {
            const params = new URLSearchParams();
            params.append('name', newRoomName);
            const response = await axios.post('http://localhost:8080/chat/room', params);

            // 새로운 방 정보를 목록에 추가
            const newRoom = response.data;
            setRooms(prevRooms => [newRoom, ...prevRooms]);
            localStorage.setItem('wschat.roomId', newRoom.roomId);
            localStorage.setItem('wschat.roomName', newRoom.name);

            navigate(`/chat/room/enter/${newRoom.roomId}`);
        } catch (error) {
            console.error('Error creating chat room:', error);
        }
    };

    const handleRoomClick = (roomId, roomName) => {
        localStorage.setItem('wschat.roomId', roomId);
        localStorage.setItem('wschat.roomName', roomName);
        navigate(`/chat/room/enter/${roomId}`);
    };

    return (
        <div className="container mt-5">
            <h2>채팅방 목록</h2>
            <form onSubmit={handleCreateRoom}>
                <div className="input-group mt-3">
                    <input
                        type="text"
                        className="form-control"
                        placeholder="채팅방 이름 입력"
                        value={newRoomName}
                        onChange={(e) => setNewRoomName(e.target.value)}
                    />
                    <div className="input-group-append">
                        <button className="btn-hover color-9" type="submit">방 생성</button>
                    </div>
                </div>
            </form>
            <div className="list-group mt-3">
                {rooms.map(room => (
                    <div key={room.roomId}
                         className="list-group-item d-flex justify-content-between align-items-center">
                        <span className="room-name">{room.name}</span>
                        <button
                            className="btn-hover color-5 btn-enter"
                            onClick={() => handleRoomClick(room.roomId, room.name)}
                        >
                            입장<i className="bi bi-emoji-smile"></i>
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
};
export default RoomList;
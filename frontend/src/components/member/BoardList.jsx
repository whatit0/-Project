import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const Community = () => {
    const [posts, setPosts] = useState([]);
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(0);
    const [board, setBoard] = useState([]);

    const refreshboard = async () => {
        try {
            const response = await axios.get('http://localhost:8080/boardListPage');

            setBoard(response.data);
        } catch (error) {
            console.error('로드 실패', error);
        }
    };
    return (
        <div className="container">
            <div className="flex">

                <div className="sub_right">
                    <div className="top sub_right_title">
                    <button onClick={refreshboard}>새로고침</button>
                        <h2>커뮤니티(중고거래)</h2>
                    </div>

                    <div className="main_list">
                        {board.map((item, index) => (
                            <div key={index}>
                                <p>No: {item.no}</p>
                                <p>Title: {item.title}</p>
                                <p>Writer: {item.writer}</p>
                                <p>Date: {item.date}</p>
                            </div>
                        ))}

                        <div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Community;

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Mypost() {
    const navigate = useNavigate();
    const [posts, setPosts] = useState([]);
    const userId = localStorage.getItem('userId');

    useEffect(() => {
        if (userId) {
            searchUserPosts();
        }
    }, [userId]);

    const searchUserPosts = async () => {
        try {
            const response = await axios.get(`http://localhost:8080/public/board/search/${userId}`);
            setPosts(response.data);
        } catch (error) {
            console.error('게시글 조회 실패', error);
        }
    };

    return (
        <>
            <h1>내 게시글</h1>
            {posts.map((post, index) => (
                <div key={index} onClick={() => navigate(`/boardDetail/${post.boardno}`)}>
                    {post.title}
                </div>
            ))}
        </>
    );
}

export default Mypost;

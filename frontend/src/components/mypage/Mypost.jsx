import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

function Mypost() {
    const navigate = useNavigate();
    const location = useLocation();
    const [posts, setPosts] = useState([]);
    const userId = location.state?.userId;
    let token = null;
    if (localStorage.getItem('accessToken')) {
        token = localStorage.getItem('accessToken');
    }

    useEffect(() => {
        if (!userId) {
            navigate('/');
        } else {
            searchUserPosts(userId);
        }
    }, [userId, navigate]);

    const searchUserPosts = async (userId) => {
        try {
            const response = await axios.post("http://localhost:8080/public/mypage/myboardlist", null, {
                params: { userid: userId }
            });
            setPosts(response.data);
        } catch (error) {
            console.error('게시글 조회 실패', error);
        }
    };

    const boardDetail = async (boardno) => {

        try {
            let response = null;
            if (token != null) {
                response = await axios.get(`http://localhost:8080/public/board/detail/token/${boardno}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                })
                navigate('/boardDetail', { state: { "data": response.data.boardData, "access": response.data.isOwner } })
            } else {
                response = await axios.get(`http://localhost:8080/public/board/detail/${boardno}`)
                navigate('/boardDetail', { state: { "data": response.data.boardData } })
            }

        } catch (error) {
            alert(error + "에러에러에러에러에러에러에러에러에러에러에러에러에러에러에러에러에러에러")
        }
    }
    return (
        <>
            <h1 className="content-title">내 게시글</h1>
            {posts.length > 0 ? (
                posts.map((post, index) => (
                    <div className="main_list">
                        <button onClick={() => boardDetail(post.boardno)}>
                            <div key={index} onClick={() => navigate(`/boardDetail/${post.boardno}`)}>
                                <p className="listNo flex_between">
                                    <span>{post.boardtitle}</span>
                                </p>
                            </div>
                        </button>
                    </div>

                ))
            ) : (
                <p>게시글이 없습니다.</p>
            )}
        </>
    );

}

export default Mypost;

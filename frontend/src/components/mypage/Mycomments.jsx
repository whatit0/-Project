import axios from "axios";
import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from "react-router-dom";



function Mycomments(){
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


    const formatDate = (dateString) => {
        const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
        const formattedDate = new Date(dateString).toLocaleDateString('en-US', options);
        return formattedDate;
    };


    const searchUserPosts = async (userId) => {
        try {
            const response = await axios.post("http://localhost:8080/public/comment/mycommentlist", null, {
                params: { userid: userId }
            });
            // alert(response.data);
            console.log("dd" + JSON.stringify(response.data, null, 2));

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
            <h1 className="content-title2">내 댓글 조회</h1>
            <p className='listTitle flex_between'>
                <span>제목</span>
            </p>
            {posts.length > 0 ? (
                posts.map((post, index) => (
                    <div className="main_list">
                        <button style={{width:"100%"}} onClick={() => boardDetail(post.boardno)}>
                            <div key={index} onClick={() => navigate(`/boardDetail/${post.boardno}`)}>
                                <p className="listNo flex_between">
                                    <span>{post.cmtcontent}</span>

                                </p>
                            </div>
                        </button>
                    </div>

                ))
            ) : (
                <p style={{padding:"20px"}}>게시글이 없습니다.</p>
            )}
        </>
    );

}

export default Mycomments;
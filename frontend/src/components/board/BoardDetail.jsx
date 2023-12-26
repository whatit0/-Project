import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router';
import { Link, useNavigate } from 'react-router-dom';
import axios from "axios";

function BoardDetail() {
    const location = useLocation();
    const boardData = location.state.data;
    const navigate = useNavigate();
    const [comments, setComments] = useState([]);
    const [commentContent, setCommentContent] = useState(''); // 댓글 내용을 위한 상태




    useEffect(() => {
        const fetchComments = async () => {
            try {
                const response = await axios.post('http://localhost:8080/public/comment/list', null, {
                    params: { boardno: boardData.boardno }
                });
                setComments(response.data);
            } catch (error) {
                console.error('Error loading comments:', error);
            }
        };

        fetchComments();
    }, [boardData.boardno]);

    let access = null;
    if(location.state.access!=null){
        access=location.state.access;
    }


    const token = localStorage.getItem('accessToken');

    const update = async (e) => {
        try {
            navigate('/boardUpdate', { state: { "data":boardData } })
        } catch (error) {
            console.error('Error during form submission:', error);
        }
    };
    const del = async()=>{
        try {
            const response = await axios.get(`http://localhost:8080/public/board/delete?boardno=${boardData.boardno}`);

            alert(response.data);
            window.location.href="/boardList";
        } catch (error) {
            console.error('Error during form submission:', error);
            alert('Error during form submission');
        }
    };
    const commentHandler = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append("boardno", boardData.boardno);
        formData.append("cmtcontent", commentContent);

        try {
            const token = localStorage.getItem('accessToken');
            await axios.post('http://localhost:8080/public/comment/write', formData, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });
            alert("댓글이 작성되었습니다.");
            setCommentContent(''); // 댓글 입력창 초기화

            // 댓글 목록 새로고침 로직
            fetchComments(); // 댓글 목록 다시 불러오기
        } catch (error) {
            console.error('댓글 작성 오류:', error);
            alert("댓글 작성 오류");
        }
    };

// 댓글 목록을 불러오는 기능을 별도의 함수로 분리
    const fetchComments = async () => {
        try {
            const response = await axios.post('http://localhost:8080/public/comment/list', null, {
                params: { boardno: boardData.boardno }
            });
            setComments(response.data);
        } catch (error) {
            console.error('Error loading comments:', error);
        }
    };

// useEffect 내에서 fetchComments 호출
    useEffect(() => {
        fetchComments();
    }, [boardData.boardno]);



    return (
        <>

            <div>
                <h2>{boardData.boardtitle}</h2>
                <p>{boardData.boardcontent}</p>
                <p>작성자: {boardData.userid}</p>
                <p>작성 날짜: {boardData.created}</p>
                <p>조회수: {boardData.boardcnt}</p>
                <img src={`/assets/${boardData.boardfilename}`}/>
            </div>
            {access === true ? <button onClick={update}>수정</button> : null}
            {access === true ? <button onClick={del}>삭제</button> : null}
            <Link to="/boardList">목록</Link>

            <h1>댓글</h1>
            {comments.map((comment, index) => (
                <div key={index}>
                    <p>{comment.userid}: {comment.cmtcontent}</p>
                </div>
            ))}

            <h1>댓글 작성</h1>
            <form onSubmit={commentHandler}>
                <label htmlFor="comment">댓글</label>
                <input
                    type="text"
                    id="comment"
                    name="comment"
                    value={commentContent}
                    onChange={(e) => setCommentContent(e.target.value)}
                />
                <button type="submit">전송</button>
            </form>
        </>
    );
}

export default BoardDetail;
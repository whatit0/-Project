import axios from "axios";
import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router';
import { Link, useNavigate } from 'react-router-dom';
import Footer from "../common/Footer";
import Header from "../common/Header";
import "../style/board.css";

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
    if (location.state.access != null) {
        access = location.state.access;
    }


    const token = localStorage.getItem('accessToken');

    const update = async (e) => {
        try {
            navigate('/boardUpdate', { state: { "data": boardData } })
        } catch (error) {
            console.error('Error during form submission:', error);
        }
    };
    const del = async () => {
        try {
            const response = await axios.get(`http://localhost:8080/public/board/delete?boardno=${boardData.boardno}`);

            alert(response.data);
            window.location.href = "/boardList";
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
        <div id="board">
            <Header />
            <div className="sub_box">
                <div className="sub_top">
                    <div className="top sub_right_title">
                        {/*<button onClick={refreshboard} style={gugin}>새로고침</button>*/}
                        <h2>COMMUNITY</h2>
                    </div>
                </div>
                <div className="board_title">
                    <h2>{boardData.boardtitle}</h2>
                    <div className="flex">
                        <p>작성자 <span>{boardData.userid}</span></p>
                        <p>작성 날짜 <span>{boardData.created}</span></p>
                        <p>조회수 <span>{boardData.boardcnt}</span></p>
                    </div>
                </div>
                <div className="board_con">
                    <p>{boardData.boardcontent}</p>
                    <img src={`/assets/${boardData.boardfilename}`} />
                </div>
                <div className="flex board_detail_btn">
                {access === true ? <button onClick={update}>수정</button> : null}
                {access === true ? <button onClick={del}>삭제</button> : null}
                <Link to="/boardList">목록</Link>
                </div>

                <h1 className="con_title">댓글</h1>
                <form onSubmit={commentHandler}>
                    <label className="away" htmlFor="comment">댓글</label>
                    <div className="flex">
                        <input
                            type="text"
                            id="comment"
                            name="comment"
                            placeholder="댓글을 작성해주세요"
                            value={commentContent}
                            onChange={(e) => setCommentContent(e.target.value)}
                        />
                        <button id="comment_btn" type="submit">댓글 작성</button>
                    </div>
                </form>
                {comments.map((comment, index) => (
                    <div key={index} className="comment_con">
                        <p>{comment.userid}: {comment.cmtcontent}</p>
                    </div>
                ))}
            </div>
            <Footer />
        </div>
    );
}

export default BoardDetail;
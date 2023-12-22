import React from 'react';
import { useLocation } from 'react-router';
import { Link, useNavigate } from 'react-router-dom';
import axios from "axios";

function BoardDetail() {
    const location = useLocation();
    const boardData = location.state.data;
    const navigate = useNavigate();
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
    const a = async()=>{

    }


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
            <form onSubmit={a}>
                <label htmlFor="boardTitle">댓글</label>
                <input
                    type="text"
                    id="comment"
                    name="comment"
                />
                <button type="submit">전송</button>
            </form>
        </>
    );
}

export default BoardDetail;
import axios from 'axios';
import React, { useState } from 'react';
import { useLocation } from "react-router";
import Footer from "../common/Footer";
import Header from "../common/Header";
import "../style/board.css";


function BoardUpdate() {
    const location = useLocation();
    const boardData = location.state.data;


    // 수정할 데이터를 위한 상태 설정
    const [title, setTitle] = useState(boardData.boardtitle);
    const [content, setContent] = useState(boardData.boardcontent);
    const [file, setFile] = useState(null);
    let boardno = boardData.boardno;

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };


    const updateRequest = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('boardtitle', title);
        formData.append('boardcontent', content);
        formData.append('boardno', boardno);
        if (file) {
            formData.append('boardFilename', file);
        }

        try {

            const response = await axios.post('http://localhost:8080/public/board/update', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
            });

            console.log(response.data);
            alert(response.data);
            window.location.href = "/boardList";

        } catch (error) {
            console.error('Error during form submission:', error);
            alert("에러에용");
            window.location.href = "/boardList";
        }
    };

    return (
        <div id='board'>
            <Header />
            <div className="sub_box">
                <div className="sub_top sub_write">
                    <div className="top sub_right_title">
                        <h2>COMMUNITY</h2>
                    </div>
                    <form onSubmit={updateRequest}>
                        {/* <div className="flex_center">
                            <p>작성자: {boardData.userid}</p>
                            <p>작성 날짜: {boardData.created}</p>
                        </div> */}
                        <div className="flex">
                            <label>제목</label>
                            <input
                                type="text"
                                name="boardTitle"
                                value={title}
                                onChange={(e) => setTitle(e.target.value)}
                            />
                        </div>
                        <div className="flex">
                            <label>내용</label>
                            <textarea
                                name="boardContent"
                                value={content}
                                onChange={(e) => setContent(e.target.value)}
                            />
                        </div>
                        {/* <p>조회수: {boardData.boardcnt}</p> */}
                        {/* <img src={`/assets/${boardData.boardfilename}`} /> */}
                        <div className="flex">
                            <label htmlFor="boardfilename">이미지 수정</label>
                            <input
                                type="file"
                                id="boardfilename"
                                name="boardfilename"
                                onChange={handleFileChange}
                            />
                        </div>

                        <button type="submit">수정하기</button>
                    </form>
                </div>
            </div >
            <Footer />
        </div >
    );
}

export default BoardUpdate;
import React, { useState } from 'react';
import { useLocation } from "react-router";
import axios from 'axios';

function BoardUpdate() {
    const location = useLocation();
    const boardData = location.state.data;



    // 수정할 데이터를 위한 상태 설정
    const [title, setTitle] = useState(boardData.boardtitle);
    const [content, setContent] = useState(boardData.boardcontent);
    const [file, setFile] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };


    const updateRequest = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('boardtitle', title);
        formData.append('boardcontent', content);
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
            window.location.href = "/boardList";

        } catch (error) {
            console.error('Error during form submission:', error);
            alert("에러에용");
            window.location.href = "/boardList";
        }
    };

    return (
        <>
            <form onSubmit={updateRequest}>
                <label>
                    제목:
                    <input
                        type="text"
                        name="boardTitle"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                    />
                </label>
                <br/>
                <label>
                    내용:
                    <textarea
                        name="boardContent"
                        value={content}
                        onChange={(e) => setContent(e.target.value)}
                    />
                </label>
                <p>작성자: {boardData.userid}</p>
                <p>작성 날짜: {boardData.created}</p>
                <p>조회수: {boardData.boardcnt}</p>
                <img src={`/assets/${boardData.boardfilename}`}/>
                <label htmlFor="boardfilename">이미지 수정</label>
                <input
                    type="file"
                    id="boardfilename"
                    name="boardfilename"
                    onChange={handleFileChange}
                />
                <br/>

                <button type="submit">수정하기</button>
            </form>
        </>
    );
}

export default BoardUpdate;
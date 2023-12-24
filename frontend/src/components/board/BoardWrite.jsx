import axios from "axios";
import React, { useState } from "react";
import Header from "../common/Header";
import "../style/board.css";

function BoardWrite() {
    const token = localStorage.getItem('accessToken');

    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const [file, setFile] = useState(null);


    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('boardtitle', title);
        formData.append('boardcontent', content);
        if (file) {
            formData.append('boardfilename', file);
        }

        try {
            const response = await axios.post('http://localhost:8080/public/board/write', formData, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'multipart/form-data'
                },
            });

            alert(response.data);
            window.location.href = "/";
        } catch (error) {
            console.error('Error during form submission:', error);
            alert('Error during form submission');
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
                    <form onSubmit={handleSubmit}>
                        <div className="flex">
                            <label htmlFor="boardTitle">제목</label>
                            <input
                                type="text"
                                id="boardtitle"
                                name="boardtitle"
                                value={title}
                                onChange={(e) => setTitle(e.target.value)}
                            />
                        </div>
                        <div className="flex">
                            <label htmlFor="boardContent">내용</label>
                            <textarea
                                id="boardcontent"
                                name="boardcontent"
                                value={content}
                                onChange={(e) => setContent(e.target.value)}
                            />
                        </div>
                        <div className="flex">
                            <label htmlFor="boardfilename">이미지</label>
                            <input
                                type="file"
                                id="boardfilename"
                                name="boardfilename"
                                onChange={handleFileChange}
                            />
                        </div>
                        <button type="submit">전송</button>
                    </form>
                </div>
            </div>
        </div>
    )
}

export default BoardWrite;
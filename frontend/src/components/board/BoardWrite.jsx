import axios from "axios";
import React, { useState } from "react";

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
        <>
            <form onSubmit={handleSubmit}>
                <label htmlFor="boardTitle">제목</label>
                <input
                    type="text"
                    id="boardtitle"
                    name="boardtitle"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                />
                <label htmlFor="boardContent">내용</label>
                <textarea
                    id="boardcontent"
                    name="boardcontent"
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                />
                <label htmlFor="boardfilename">이미지</label>
                <input
                    type="file"
                    id="boardfilename"
                    name="boardfilename"
                    onChange={handleFileChange}
                />
                <button type="submit">전송</button>
            </form>
        </>
    )
}

export default BoardWrite;
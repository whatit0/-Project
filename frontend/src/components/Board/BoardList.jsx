import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

function BoardList() {
    const [posts, setPosts] = useState([]);
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(0);
    const [board, setBoard] = useState([]);

    const refreshboard = async () => {
        try {
            const response = await axios.get('http://localhost:8080/board/test');
            // console.log(response.data);
            setBoard(response.data);
        } catch (error) {
            console.error('로드 실패', error);
        }
    };
    const boardDetail = async (postno) => {
        try{
            const response = await axios.get(`http://localhost:8080/board/detail${postno}`)
        }catch(error){

        }
    }
    return (
        <div className="container">
            <div className="flex">

                <div className="sub_right">
                    <div className="top sub_right_title">
                        <button onClick={refreshboard}>새로고침</button>
                        <h2>커뮤니티(중고거래)</h2>
                    </div>
                    <div className="main_list">
                        <p>번호</p>
                        <p>제목</p>
                        <p>작성자</p>
                        <p>작성 날짜</p>
                        <p>조회</p>
                        {board.map((item, index) => (
                            <div key={index} className="boardList">
                                <button onClick={() => boardDetail(item.postno)}>

                                    <p className="listNo">No: {item.postno}</p>
                                    <p>Title: {item.posttitle}</p>
                                    <p>Writer: {item.writer}</p>
                                    <p>Date: {item.created}</p>
                                    <p>Count: {item.postcnt}</p>
                                </button>
                            </div>
                        ))}

                        <div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default BoardList;

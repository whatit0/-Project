import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';
// import './Paging.css';
import Pagination from "react-js-pagination";

function BoardList() {
    const navigate = useNavigate();
    const [posts, setPosts] = useState([]);
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(0);
    const [board, setBoard] = useState([]);
    let token = null;
    if(localStorage.getItem('accessToken')){
     token = localStorage.getItem('accessToken');
    }


    const refreshboard = async () => {
        try {
            const response = await axios.get('http://localhost:8080/public/board/test');
            setBoard(response.data);
        } catch (error) {
            console.error('로드 실패', error);
        }
    };

    const boardDetail = async (boardno) => {

        try{
            let response = null;
            if(token!=null){
                response = await axios.get(`http://localhost:8080/public/board/detail/token/${boardno}`,{
                headers: {
                    'Authorization': `Bearer ${token}`},
                })
                    navigate('/boardDetail', { state: { "data":response.data.boardData,"access":response.data.isOwner } })
            }else{
                 response = await axios.get(`http://localhost:8080/public/board/detail/${boardno}`)
                navigate('/boardDetail', { state: { "data":response.data.boardData } })
            }

        }catch(error){
            alert(error+"에러에러에러에러에러에러에러에러에러에러에러에러에러에러에러에러에러에러")
        }
    }
    const gugin = {
        width: 500,
        height: 300,
        color: "black",
        fontSize: 140,
        backgroundColor: "hotpink",
    }
    const handlePageChange = (pageNumber) => {
        setPage(pageNumber);
    };

    return (
        <div className="container">
            <div className="flex">
                <div className="sub_right">
                    <div className="top sub_right_title">
                        <button onClick={refreshboard} style={gugin}>새로고침</button>
                        <h2>커뮤니티(중고거래)</h2>
                    </div>
                    <div className="main_list">
                        <p>
                            <span>번호</span>
                            <span>제목</span>
                            <span>작성자</span>
                            <span>작성 날짜</span>
                            <span>조회</span>
                        </p>
                        {board.map((item, index) => (
                            <div key={index} className="boardList">
                                <button onClick={() => boardDetail(item.boardno)}>
                                    <p className="listNo">
                                        <span>No: {item.boardno}</span>
                                        <span>Title: {item.boardtitle}</span>
                                        <span>Writer: {item.writer}</span>
                                        <span>Date: {item.created}</span>
                                        <span>Count: {item.boardcnt}</span>
                                    </p>
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
            <Pagination
                activePage={page}
                itemsCountPerPage={10}
                totalItemsCount={450}
                pageRangeDisplayed={5}
                prevPageText={"‹"}
                nextPageText={"›"}
                onChange={handlePageChange}
            />
        </div>
    );
}

export default BoardList;
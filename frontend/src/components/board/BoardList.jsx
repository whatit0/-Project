import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';
import Pagination from "react-js-pagination";

function BoardList() {
    const navigate = useNavigate();
    const [posts, setPosts] = useState([]);
    const [totalPages, setTotalPages] = useState(0);
    const [board, setBoard] = useState([]);
    const [currentBoard, setCurrentBoard] = useState([]);
    const [page, setPage] = useState(1);
    const [type, setType] = useState('writer');
    const [title, setTitle] = useState('');
    const [searchResults, setSearchResults] = useState([]); // 검색 결과를 저장할 상태 변수
    const itemsPerPage = 10;
    let token = null;
    if(localStorage.getItem('accessToken')){
     token = localStorage.getItem('accessToken');
    }


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

    const search = async () => {
        const data = new FormData();
        data.append("type",type);
        data.append("title",title);

        if(title===''){
            setSearchResults('');
        }else{

            const response = await axios.post('http://localhost:8080/public/board/search', data);
            alert('dd');
            alert(response.data);
            if(response.data==="zero"){
                alert("검색 결과가 없어요."); // 테스트용
                setSearchResults(null);
            }else{
            setSearchResults(response.data);
            }


        }
    }

    useEffect(() => {
        const fetchBoard = async () => {
            try {
                const response = await axios.get('http://localhost:8080/public/board/test');
                setBoard(response.data);
                setCurrentBoard(response.data.slice((page - 1) * itemsPerPage, page * itemsPerPage));
            } catch (error) {
                console.error('ewdwfewewfwwef', error);
            }
        };
        fetchBoard();
    }, [page]);

    const handlePageChange = (pageNumber) => {
        setPage(pageNumber);
        setCurrentBoard(board.slice((pageNumber - 1) * itemsPerPage, pageNumber * itemsPerPage));
    };

    return (
        <div className="container">
            <div className="flex">
                <div className="sub_right">
                    <div className="top sub_right_title">
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

                        {(searchResults.length > 0 ? searchResults : board)
                            .slice((page - 1) * itemsPerPage, page * itemsPerPage)
                            .map((item, index) => (
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
                itemsCountPerPage={itemsPerPage}
                totalItemsCount={(searchResults.length > 0 ? searchResults : board).length}
                pageRangeDisplayed={5}
                prevPageText={"‹"}
                nextPageText={"›"}
                onChange={handlePageChange}
            />
            <div className="search">
                <form onSubmit={search}>
                    <p>
                        <span>
                            <label htmlFor="searchType">검색</label>
                            <select id="searchType" onChange={(e) => setType(e.target.value)} value={type}>
                                <option value="writer" >작성자</option>
                                <option value="title">제목</option>
                            </select>
                        </span>
                        <span>
                            <label htmlFor="searchtitle">검색 내용</label>
                            <input
                                type="text"
                                id="searchtitle"
                                onChange={(e) => setTitle(e.target.value)}
                            />
                        </span>
                        <span><button type="submit">검색</button></span>
                    </p>
                </form>
            </div>

        </div>
    );
}

export default BoardList;
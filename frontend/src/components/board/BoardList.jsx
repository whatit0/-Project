import axios from 'axios';
import React, { useEffect, useState } from 'react';
import Pagination from "react-js-pagination";
import { Link, useNavigate } from 'react-router-dom';
import Header from "../common/Header";
import "../style/board.css";


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
    if (localStorage.getItem('accessToken')) {
        token = localStorage.getItem('accessToken');
    }


    const boardDetail = async (boardno) => {

        try {
            let response = null;
            if (token != null) {
                response = await axios.get(`http://localhost:8080/public/board/detail/token/${boardno}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                })
                navigate('/boardDetail', { state: { "data": response.data.boardData, "access": response.data.isOwner } })
            } else {
                response = await axios.get(`http://localhost:8080/public/board/detail/${boardno}`)
                navigate('/boardDetail', { state: { "data": response.data.boardData } })
            }

        } catch (error) {
            alert(error + "에러에러에러에러에러에러에러에러에러에러에러에러에러에러에러에러에러에러")
        }
    }

    const search = (event) => {
        event.preventDefault();
        const data = new FormData();
        data.append("type", type);
        data.append("title", title);
        axios.post('http://localhost:8080/public/board/search', data)
            .then(response => {
                if (response.data.length > 0) {
                    setSearchResults(response.data);
                } else {
                    alert("검색 결과가 없어요."); // 테스트용
                }
            })
            .catch(error => {
                alert("error");
                console.error('검색 실패', error);
            });
    };



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

    const formatDate = (dateString) => {
        const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
        return new Date(dateString).toLocaleDateString(undefined, options);
    };

    return (
        <div id='board'>
            <Header />
            <div className="sub_box">
                <div className="sub_top">
                    <div className="top sub_right_title">
                        <h2>COMMUNITY</h2>
                    </div>
                    <div className="search">
                        <form onSubmit={search}>
                            <p>
                                <span>
                                    <label className='away' htmlFor="searchType">검색</label>
                                    <select id="searchType" onChange={(e) => setType(e.target.value)}>
                                        <option value="writer">작성자</option>
                                        <option value="title">제목</option>
                                    </select>
                                </span>
                                <span className='search_area'>
                                    <label className='away' htmlFor="searchtitle">검색 내용</label>
                                    <input
                                        type="text"
                                        id="searchtitle"
                                        placeholder='검색어를 입력해주세요'
                                        onChange={(e) => setTitle(e.target.value)}
                                    />
                                    <button type="submit"><span className="material-symbols-rounded fs25">search</span></button>
                                </span>
                            </p>
                        </form>
                    </div>
                </div>
                <div style={{width:"100%", textAlign:"right"}}><Link className='write_btn' to="/boardwrite">글쓰기</Link></div>
                <div className="main_list">
                    <p className='main_list_column flex_between'>
                        <span>번호</span>
                        <span className='b_subject tacen'>제목</span>
                        <span>작성자</span>
                        <span>작성일</span>
                        <span>조회수</span>
                    </p>

                    {(searchResults.length > 0 ? searchResults : board)
                        .slice((page - 1) * itemsPerPage, page * itemsPerPage)
                        .map((item, index) => (
                            <div key={index} className="boardList">
                                <button onClick={() => boardDetail(item.boardno)}>
                                    <p className="listNo flex_between">
                                        <span>{item.boardno}</span>
                                        <span className='b_subject'>{item.boardtitle}</span>
                                        <span>{item.userid}</span>
                                        <span>{formatDate(item.created)}</span>
                                        <span>{item.boardcnt}</span>
                                    </p>
                                </button>
                            </div>
                        ))}
                </div>
                <div className="page_con">
                    <Pagination
                        activePage={page}
                        itemsCountPerPage={itemsPerPage}
                        totalItemsCount={(searchResults.length > 0 ? searchResults : board).length}
                        pageRangeDisplayed={5}
                        prevPageText={<span className='material-symbols-rounded gray'>chevron_left</span>}
                        nextPageText={<span className='material-symbols-rounded gray'>chevron_right</span>}
                        onChange={handlePageChange}
                    />
                </div>
            </div>
        </div>
    );
}

export default BoardList;
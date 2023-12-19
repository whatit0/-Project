import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from "axios";

function Home() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const token1 = localStorage.getItem('accessToken');
    const token2 = localStorage.getItem('expiresIn');
    useEffect(() => {

        if (token1 && token2) {
            // 토큰 유효성 검증 로직 (옵션)
            setIsLoggedIn(true);
        }
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('expiresIn');
        setIsLoggedIn(false);

    };

    const boardPage = async () => {
        try {
            const response = await axios.post('http://localhost:8080/public/board/boardPage', {
                accessToken: token1,
                expiresIn: token2,
            }, {
                withCredentials: true,  // CORS 문제 해결을 위해 추가
            });


         window.location.href="/boardList";

        } catch (error) {
            console.error('Error during login:', error);
        }
    };


    const d = localStorage.getItem('accessToken');
    const c = localStorage.getItem('expiresIn');

    return (
        <>
            <div>
                {isLoggedIn ? (
                    <button onClick={handleLogout}>로그아웃</button>
                ) : (
                    <button onClick={() => window.location.href = '/loginPage'}>로그인</button>
                )}
            </div>

            <Link to="/registerPage">회원가입</Link>
            <button onClick={boardPage}>게시판</button>
            <Link to="/boardList">게시판</Link>
            <p>현재 토큰 정보 : </p>
            <p>{d}</p>
            <p>{c}</p>
        </>
    );
}

export default Home;

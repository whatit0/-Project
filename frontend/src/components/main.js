import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

function Home() {

    return (
        <>
                <Link to="/loginPage">로그인</Link>
                <Link to="/registerPage">회원가입</Link>
                <Link to="/chatList">채팅방</Link>
                <Link to="/boardList">게시판</Link>
                <Link to="/map">지도</Link>
        </>
    );
}

export default Home;

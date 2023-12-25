import React, {Component, useEffect, useState} from 'react';
import { Link } from 'react-router-dom';
import "../style/base.css";
import "../style/common.css";
import Home from "../main";

function Header() {

    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const token1 = localStorage.getItem('accessToken');

    useEffect(() => {

        if (token1) {
            // 토큰 유효성 검증 로직 (옵션)
            setIsLoggedIn(true);
        }
    }, []);
    const handleLogout = () => {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('expiresIn');
        setIsLoggedIn(false);

    };
        return (

            <div id='header' className='flex'>
                <div id="logo"><Link to="/" className='fs20 white'>LOGO</Link></div>
                <div id="h_menu" className='flex'>
                    <Link to="/" className="h_menu_list h_menu01">HOME</Link>
                    <Link to="/chatList" className="h_menu_list h_menu02">CHATTING</Link>
                    <Link to="/boardList" className="h_menu_list h_menu03">COMMUNITY</Link>
                    <Link to="/" className="h_menu_list h_menu04">NOTICE</Link>
                    <Link to="/mypage" className="h_menu_list h_menu05">MYPAGE</Link>
                </div>
                <div id="h_auth" className='flex'>
                    {isLoggedIn ? (
                        <button onClick={handleLogout}>로그아웃</button>
                    ) : (
                        <>
                        <Link to="/loginPage" className="h_auth_list h_auth01">로그인</Link>
                        <span>|</span>
                        <Link to="/registerPage" className="h_auth_list h_auth02">회원가입</Link>
                        </>
                    )}
                </div>
            </div>
        );

}

export default Header;
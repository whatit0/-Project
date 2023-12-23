import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import "../style/base.css";
import "../style/common.css";

class Header extends Component {
    render() {
        return (
            <div id='header' className='flex'>
                <div id="logo"><Link to="/" className='fs35'>나랑따릉</Link></div>
                <div id="h_menu" className='flex'>
                    <Link to="/map" className="h_menu_list h_menu01">홈</Link>
                    <Link to="/chatList" className="h_menu_list h_menu02">채팅</Link>
                    <Link to="/" className="h_menu_list h_menu03">커뮤니티</Link>
                    {/* <Link to="/" className="h_menu_list h_menu04">공지사항</Link> */}
                    <Link to="/" className="h_menu_list h_menu05">마이페이지</Link>
                </div>
                <div id="h_auth" className='flex'>
                    <Link to="/login" className="h_auth_list h_auth01">로그인</Link>
                    <span>|</span>
                    <Link to="/" className="h_auth_list h_auth02">회원가입</Link>
                </div>
            </div>
        );
    }
}

export default Header;
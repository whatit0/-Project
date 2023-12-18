import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import "../style/base.css";
import "../style/common.css";

class Header extends Component {
    render() {
        return (
            <div id='header' className='flex'>
                <div id="logo"><Link to="/" className='fs20 white'>LOGO</Link></div>
                <div id="h_menu" className='flex'>
                    <Link to="/" className="h_menu_list h_menu01">HOME</Link>
                    <Link to="/" className="h_menu_list h_menu02">CHATTING</Link>
                    <Link to="/" className="h_menu_list h_menu03">COMMUNITY</Link>
                    <Link to="/" className="h_menu_list h_menu04">NOTICE</Link>
                    <Link to="/" className="h_menu_list h_menu05">MYPAGE</Link>
                </div>
                <div id="h_auth" className='flex'>
                    <Link to="/" className="h_auth_list h_auth01">로그인</Link>
                    <span>|</span>
                    <Link to="/" className="h_auth_list h_auth02">회원가입</Link>
                </div>
            </div>
        );
    }
}

export default Header;
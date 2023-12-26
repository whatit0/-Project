import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import Footer from "../common/Footer";
import Header from "../common/Header";
import '../style/mypage.css';
import DeleteAccount from './DeleteAccount';
import EditUser from './Edituser';
import MyComments from './Mycomments';
import Mypost from './Mypost';

function Mypage() {
    const [selectedMenuItem, setSelectedMenuItem] = useState('edituser');
    const location = useLocation();
    const userId = location.state?.userId; // 이전 페이지에서 전달받은 userId

    useEffect(() => {
        // userId가 없으면 로그인 페이지로 리다이렉션
        if (!userId) {
            window.location.href = "/";
            alert("로그인을 하세요 제발 ");
        }
    }, [userId]);


    const renderComponent = () => {
        switch(selectedMenuItem) {
            case 'edituser':
                return <EditUser />;
            case 'myposts':
                return <Mypost />;
            case 'mycomments':
                return <MyComments />;
            case 'deleteaccount':
                return <DeleteAccount />;
            default:
                return <div>선택된 항목이 없습니다.</div>;
        }
    };

    return (
        <div id="mypage">
            <Header />
            <div className="sub_top">
                <div className="top sub_right_title">
                    <h2>MY PAGE</h2>
                </div>
            </div>
            <div className="mypage-container">
                <div className="mypage-sidebar">
                    <p>나의 정보</p>
                    <ul className="mypage-menu">
                        <li onClick={() => setSelectedMenuItem('edituser')}>회원정보 수정</li>
                        <li onClick={() => setSelectedMenuItem('myposts')}>내 게시글 조회</li>
                        <li onClick={() => setSelectedMenuItem('mycomments')}>내 댓글 조회</li>
                        <li onClick={() => setSelectedMenuItem('deleteaccount')}>회원 탈퇴</li>
                    </ul>
                </div>
                <div className="mypage-content">
                    {renderComponent()}
                </div>
            </div>
            <Footer />
        </div>
        
    );
}

export default Mypage;

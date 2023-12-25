import React, { useState } from 'react';
import '../style/mypage.css';
import EditUser from './Edituser';
import Mypost from './Mypost';
import MyComments from './Mycomments';
import DeleteAccount from './DeleteAccount';

function Mypage() {
    const [selectedMenuItem, setSelectedMenuItem] = useState('edituser');

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
        <div className="mypage-container">
            <div className="mypage-sidebar">
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
    );
}

export default Mypage;

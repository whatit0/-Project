import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from "axios";


function Edituser(){
    const navigate = useNavigate();
    const location = useLocation();
    const userId = location.state?.userId;

    const [originPassword, setOriginPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [phone, setPhone] = useState('');


    const handleOriginPasswordChange = (e) => {
        setOriginPassword(e.target.value);
    };

    const handleNewPasswordChange = (e) => {
        setNewPassword(e.target.value);
    };

    const handleConfirmPasswordChange = (e) => {
        setConfirmPassword(e.target.value);
    };

    const handlePhoneChange = (e) => {
        setPhone(e.target.value);
    };

    const handlerUserUpdate = async (e) => {
        e.preventDefault();

        if (newPassword !== confirmPassword) {
            alert("새 비밀번호가 일치하지 않습니다.");
            return;
        }

        try {
            const response = await axios.post("http://localhost:8080/public/user/update", null, {
                params: {
                    userid: userId,
                    originuserPwd: originPassword,
                    userPwd: newPassword,
                    userTel: phone
                }
            });
            alert(response.data);
            if(response.data === "두둥탁성공"){
                localStorage.removeItem('accessToken');
                localStorage.removeItem('expiresIn');
                window.location.href="/";
            }

        } catch (error) {
            console.error('Update failed', error);
        }
    };
    return(
        <>
            <div className="mypage-content">
                <h1 className="content-title">개인 정보 수정</h1>
                <form className="info-form" onSubmit={handlerUserUpdate}>
                    <label className="form-label">
                        <span>아이디</span>
                        <input type="text" className="form-input"value={userId} readOnly />
                    </label>
                    <label className="form-label">
                        <span>비밀번호</span>
                        <input
                            type="password"
                            className="form-input"
                            placeholder="현재 비밀번호를 입력하세요"
                            onChange={handleOriginPasswordChange}
                        />
                    </label>
                    <label className="form-label">
                        <span>새 비밀번호</span>
                        <input
                            type="password"
                            className="form-input"
                            placeholder="새 비밀번호를 입력하세요"
                            onChange={handleNewPasswordChange}
                        />
                    </label>
                    <label className="form-label">
                        <span>새 비밀번호 확인</span>
                        <input
                            type="password"
                            className="form-input"
                            placeholder="새 비밀번호를 다시 입력하세요"
                            onChange={handleConfirmPasswordChange}
                        />
                    </label>
                    <label className="form-label">
                        <span>전화번호</span>
                        <input
                            type="tel"
                            className="form-input"
                            placeholder="전화번호를 입력하세요"
                            onChange={handlePhoneChange}
                        />
                    </label>
                    <div style={{width : "100%", textAlign: "center"}}><button type="submit" className="form-submit">변경사항 저장</button></div>
                </form>
            </div>
        </>
    )

}


export default Edituser;
import React, { useState } from 'react';
import axios from 'axios';
// import '../style/register.css';

function RegisterPage() {
    const [userData, setUserData] = useState({
        userId: '',
        userName: '',
        userNickname: '',
        userPwd: '',
        userPwdConfirm: '',
        userGender: 'M',
        userTel: '',
        userAge: ''
    });

    const [isPwdMatch, setIsPwdMatch] = useState(true);
    const [isUserIdAvailable, setIsUserIdAvailable] = useState(true)
    const [userIdCheckMessage, setUserIdCheckMessage] = useState(null);

    const handleChange = (e) => {
        setUserData({ ...userData, [e.target.name]: e.target.value });

        if (e.target.name === 'userPwd' || e.target.name === 'userPwdConfirm') {
            setIsPwdMatch(userData.userPwd === e.target.value || e.target.value === '');
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            console.log("1111111")
            const response = await axios.post('http://localhost:8080/public/user/registerRequest',
                userData,
                {   withCredentials: true,  // CORS 문제 해결을 위해 추가
            });
            console.log("2222222")
            console.log(response.data);
            window.location.href = '/loginPage'; // 메인 페이지로 리다이렉트
        } catch (error) {
            console.error('회원가입 실패:', error);
        }
    };


    const checkUserIdAvailability = async () => {
        try {
            const response = await axios.post('http://localhost:8080/hidden/user/registerIdCheck',
                { userId: userData.userId },
                {   withCredentials: true,  }
            );
            const message = response.data.message;
            setUserIdCheckMessage(message);
            setIsUserIdAvailable(message === "사용 가능한 아이디 입니다.");
        } catch (error) {
            console.error('아이디 중복 확인 실패:', error);
            setUserIdCheckMessage(null); // 오류가 발생한 경우 메시지 초기화
        }
    };


    const isFormValid = () => {
        return userData.userId && userData.userName && userData.userNickname && userData.userPwd &&
            userData.userPwdConfirm && userData.userTel && userData.userAge && isPwdMatch && isUserIdAvailable;
    };


    return (
        <div className="signup-container">
            <form onSubmit={handleSubmit}>
                <h2>회원가입</h2>

                <div className="input-group">
                    <label htmlFor="userId">아이디</label>
                    <input
                        type="text"
                        id="userId"
                        name="userId"
                        value={userData.userId}
                        onChange={handleChange}
                    />
                    <button type="button" onClick={checkUserIdAvailability}>아이디 중복 확인</button>

                    {
                        userIdCheckMessage && (
                            <div className={isUserIdAvailable ? "success-message" : "error-message"}>
                                {userIdCheckMessage}
                            </div>
                        )
                    }
                </div>
                <div className="input-group">
                    <label htmlFor="userName">이름</label>
                    <input
                        type="text"
                        id="userName"
                        name="userName"
                        value={userData.userName}
                        onChange={handleChange}
                    />
                </div>
                <div className="input-group">
                    <label htmlFor="userNickname">닉네임</label>
                    <input
                        type="text"
                        id="userNickname"
                        name="userNickname"
                        value={userData.userNickname}
                        onChange={handleChange}
                    />
                </div>
                <div className="input-group">
                    <label htmlFor="userPwd">비밀번호</label>
                    <input
                        type="password"
                        id="userPwd"
                        name="userPwd"
                        value={userData.userPwd}
                        onChange={handleChange}
                    />
                </div>
                <div className="input-group">
                    <label htmlFor="userPwdConfirm">비밀번호 확인</label>
                    <input
                        type="password"
                        id="userPwdConfirm"
                        name="userPwdConfirm"
                        value={userData.userPwdConfirm}
                        onChange={handleChange}
                    />
                    {!isPwdMatch && <div className="error-message">비밀번호가 일치하지 않습니다.</div>}
                </div>
                <div className="input-group">
                    <label htmlFor="userGender">성별</label>
                    <select
                        id="userGender"
                        name="userGender"
                        value={userData.userGender}
                        onChange={handleChange}
                    >
                        <option value="M">남자</option>
                        <option value="F">여자</option>
                    </select>
                </div>
                <div className="input-group">
                    <label htmlFor="userTel">전화번호</label>
                    <input
                        type="tel"
                        id="userTel"
                        name="userTel"
                        value={userData.userTel}
                        onChange={handleChange}
                    />
                </div>
                <div className="input-group">
                    <label htmlFor="userAge">나이</label>
                    <input
                        type="number"
                        id="userAge"
                        name="userAge"
                        value={userData.userAge}
                        onChange={handleChange}
                    />
                </div>
                <button type="submit" disabled={!isFormValid()}>회원가입</button>
            </form>
        </div>
    );
}

export default RegisterPage;

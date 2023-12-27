import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import '../style/login.css';

function LoginPage(props) {
    const [userId, setUserId] = useState('');
    const [userPwd, setUserPwd] = useState('');
    const [isButtonDisabled, setIsButtonDisabled] = useState(true);

    useEffect(() => {
        const isUserIdValid = /^[a-z0-9]{1,12}$/.test(userId);
        const isUserPwdValid = /^[a-z0-9]{1,12}$/.test(userPwd);
        setIsButtonDisabled(!(isUserIdValid && isUserPwdValid));
    }, [userId, userPwd]);

    const loginRequest = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:8080/public/user/loginRequest', {
                userId: userId,
                userPwd: userPwd,
            }, {
                withCredentials: true,  // CORS 문제 해결을 위해 추가
            });
            console.log(response.data.accessToken);
            console.log(response.data.expiresIn);
            const token = response.data;
            const dd = response.data.accessToken;
            const kk = response.data.expiresIn;
            if (response.data === null) {
                // 기존 페이지 유지 및 경고 표시 (로그인 실패)
                alert('로그인에 실패했습니다.');
            } else {
                // localStorage.setItem('jwtToken', token);
                localStorage.setItem('accessToken', dd);
                localStorage.setItem('expiresIn', kk);
                window.location.href = '/'; // 메인 페이지로 리다이렉트
            }

        } catch (error) {
            console.error('Error during login:', error);
        }
    };


    return (
        <form onSubmit={loginRequest}>
            <div className="login-container">
                <div className="login-title">Log In</div>
                <div className="login-form">
                    <div className="input-container">
                        <div className="username-field">
                            <div className="input-wrapper flex">
                                <span class="material-symbols-rounded fw400 li-gray">account_circle</span>
                                <input
                                    id="userid"
                                    placeholder="아이디를 입력하세요"
                                    className="input-field"
                                    value={userId}
                                    onChange={(e) => setUserId(e.target.value)}
                                    required
                                />
                            </div>
                        </div>
                        <div className="password-field">
                            <div className="input-wrapper flex">
                                <span class="material-symbols-rounded fw400 li-gray">lock</span>
                                <input
                                    id="userpwd"
                                    placeholder="비밀번호를 입력하세요"
                                    className="input-field"
                                    type="password"
                                    value={userPwd}
                                    onChange={(e) => setUserPwd(e.target.value)}
                                    required
                                />
                            </div>
                        </div>
                    </div>
                    <div className="link-container">
                        <Link to="/id_search" className="find-username-link">
                            아이디 찾기
                        </Link>
                        <span className="divider"></span>
                        <Link to="/passwd_search" className="find-password-link">
                            비밀번호 찾기
                        </Link>
                    </div>
                    <div className="button-container flex" style={{justifyContent:"center"}}>
                        <button className="login-button" type="submit" id="btnLogin" disabled={isButtonDisabled}>
                            <span className="button-text">로그인</span>
                        </button>
                        <Link to="/registerPage" className="signup-button">
                            <button type="button" onClick={() => (window.location.href = '/registerPage')}>
                                <span className="button-text">회원가입</span>
                            </button>
                        </Link>
                    </div>
                </div>
            </div>
        </form>
    );
}

export default LoginPage;

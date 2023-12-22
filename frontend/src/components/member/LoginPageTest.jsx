import axios from 'axios';
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useMutation } from 'react-query';
import '../style/login.css';

const LoginPageTest = () => {

    const navigate = useNavigate();
    const [loginUser, setLoginUser] = useState({ userId:"",password:""});
    const [errorMessages, setErrorMessages] = useState({ userId:"", password:"" });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setLoginUser({ ...loginUser, [name]:value });
    }

    const login = useMutation(async (loginUser) => {
        try {
            const response = await axios.post("http://localhost:8080/user/loginRequest", loginUser);
            setErrorMessages({userId: "", password: "" ,  });
            return response;
        } catch(error) {
            if(error.response.status === 401) {
                alert("사용자 정보를 확인해주세요.");
            }
            setErrorMessages({userId: "", password: "", ...error.response.data.errorData});
            return error;
        }
    }, {
        onSuccess: (response) => {
            if(response.status === 200) {
                localStorage.setItem("accessToken", response.data);
                navigate("/");
            }
        }
    });

    const
        loginHandleSubmit = async() => {
            login.mutate(loginUser);
        }

    const googleAuthClickHandle = () => {
        window.location.href="http://localhost:8080/oauth2/authorization/google";
    }

    const naverAuthCliclkHandle = () => {
        window.location.href="http://localhost:8080/oauth2/authorization/naver";
    }

    const kakaoAuthClickHandle = () => {
        window.location.href="http://localhost:8080/oauth2/authorization/kakao";
    }


    return (
        <div className="container">
            <header>
                <div className="headerContainer">
                    <h1 className="title">
                        <div className="logoStyle" />
                    </h1>
                </div>
            </header>
            <main className="mainContainer">
                <div>
                    <label className="inputLabel">아이디</label>
                    <input type="userId" placeholder="Type your userId" onChange={handleChange} name="userId" />
                    <div className="errorMsg">{errorMessages.userId}</div>
                    <label className="inputLabel">비밀번호</label>
                    <input type="password" placeholder="Type your password" onChange={handleChange} name="password" />
                    <div className="errorMsg">{errorMessages.password}</div>
                    <div className="forgetPassword">
                        <div className="link-container">
                            <Link to="/id_search" className="find-username-link">
                                아이디 찾기
                            </Link>
                            <span className="divider"></span>
                            <Link to="/passwd_search" className="find-password-link">
                                비밀번호 찾기
                            </Link>
                        </div>
                    </div>
                    <button className="loginButton" onClick={loginHandleSubmit}>로그인</button>
                    <button className="loginButton" onClick={() => (window.location.href = '/registerPage')}>회원가입</button>
                </div>

                <div></div>
            </main>



            <footer className="footerStyles">
                <div className="register">
                    <Link to="/registerPage">
                        <button type="button" onClick={() => (window.location.href = '/registerPage')} className="signup-button">
                            <span className="button-text">회원가입</span>
                        </button>
                    </Link>
                </div>
            </footer>
        </div>
    );

};

export default LoginPageTest;
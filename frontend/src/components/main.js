import React from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

function Home() {

    const loginPageRequest = async () => {
        try {
            // console.log("dsafds")
            const response = await axios.post('http://localhost:8080/public/loginPageRequest', {
                withCredentials: true,
            });

            console.log(response.data);

            if (response.data === 'abcd') {
                window.location.href = '/loginPage';
            } else {
                alert('오류.');
            }
        } catch (error) {
            console.error('Error : ', error);
        }
    }

    return (
        <>
            <button onClick={loginPageRequest}>로그인</button>

            <Link to="/loginPageTest">로그인</Link>
            <Link to="/registerPage">회원가입</Link>
            <Link to="/boardList">게시판</Link>
        </>
    );
}

export default Home;

import React from 'react';
import { Link } from 'react-router-dom';

function Home() {

    return (
        <>
                <Link to="/loginPage">로그인</Link>
                <Link to="/registerPage">회원가입</Link>


        </>
    );
}




export default Home;

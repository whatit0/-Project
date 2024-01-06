import React, { useState } from 'react';
import axios from 'axios';
// import '../style/register.css';

function RegisterPage() {

    const styles = {
        container: {
            maxWidth: '500px',
            margin: '40px auto',
            padding: '20px',
            border: '1px solid #ddd',
            borderRadius: '4px',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
            textAlign: 'left',
            backgroundColor: '#fff'
        },
        title: {
            textAlign: 'center',
            marginBottom: '20px'
        },
        inputGroup: {
            marginBottom: '15px',
        },
        label: {
            display: 'block',
            marginBottom: '5px',
            fontWeight: 'bold'
        },
        input: {
            width: '100%',
            padding: '10px',
            border: '1px solid #ddd',
            borderRadius: '4px',
            boxSizing: 'border-box'
        },
        button: {
            width: '100%',
            padding: '10px',
            backgroundColor: 'hotpink',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            marginTop: '20px'
        },
        errorMessage: {
            color: 'red',
            fontSize: '14px',
        },
        successMessage: {
            color: 'green',
            fontSize: '14px',
        },
        buttonCheck: {
            backgroundColor: 'hotpink',
            border: 'none',
            color: 'white',
            padding: '8px 12px',
            marginLeft: '10px',
            borderRadius: '4px',
            cursor: 'pointer'
        }
    };


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
            const response = await axios.post('http://localhost:8080/public/user/registerRequest',
                userData,
                {   withCredentials: true,  // CORS 문제 해결을 위해 추가
            });
            window.location.href = '/loginPage'; // 메인 페이지로 리다이렉트
        } catch (error) {
            console.error('회원가입 실패:', error);
        }
    };


    const checkUserIdAvailability = async () => {
        try {
            const response = await axios.post('http://localhost:8080/public/user/registerIdCheck',
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
        <div style={styles.container}>
            <form onSubmit={handleSubmit}>
                <h2 style={styles.title}>회원가입</h2>

                <div style={styles.inputGroup}>
                    <label htmlFor="userId" style={styles.label}>아이디</label>
                    <div style={{ display: 'flex', alignItems: 'center' }}>
                        <input
                            type="text"
                            id="userId"
                            name="userId"
                            style={{ ...styles.input, flex: 1 }}
                            onChange={handleChange}
                        />
                        <button type="button" style={styles.buttonCheck} onClick={checkUserIdAvailability}>중복검사</button>
                    </div>
                    {userIdCheckMessage && (
                        <div style={isUserIdAvailable ? styles.successMessage : styles.errorMessage}>
                            {userIdCheckMessage}
                        </div>
                    )}
                </div>

                <div style={styles.inputGroup}>
                    <label htmlFor="userName" style={styles.label}>이름</label>
                    <input
                        type="text"
                        id="userName"
                        name="userName"
                        style={styles.input}
                        value={userData.userName}
                        onChange={handleChange}
                    />
                </div>

                <div style={styles.inputGroup}>
                    <label htmlFor="userNickname" style={styles.label}>닉네임</label>
                    <input
                        type="text"
                        id="userNickname"
                        name="userNickname"
                        style={styles.input}
                        value={userData.userNickname}
                        onChange={handleChange}
                    />
                </div>

                <div style={styles.inputGroup}>
                    <label htmlFor="userPwd" style={styles.label}>비밀번호</label>
                    <input
                        type="password"
                        id="userPwd"
                        name="userPwd"
                        style={styles.input}
                        value={userData.userPwd}
                        onChange={handleChange}
                    />
                </div>

                <div style={styles.inputGroup}>
                    <label htmlFor="userPwdConfirm" style={styles.label}>비밀번호 확인</label>
                    <input
                        type="password"
                        id="userPwdConfirm"
                        name="userPwdConfirm"
                        style={styles.input}
                        value={userData.userPwdConfirm}
                        onChange={handleChange}
                    />
                    {!isPwdMatch && (
                        <div style={styles.errorMessage}>비밀번호가 일치하지 않습니다.</div>
                    )}
                </div>

                <div style={styles.inputGroup}>
                    <label htmlFor="userGender" style={styles.label}>성별</label>
                    <select
                        id="userGender"
                        name="userGender"
                        style={styles.input}
                        value={userData.userGender}
                        onChange={handleChange}
                    >
                        <option value="M">남자</option>
                        <option value="F">여자</option>
                    </select>
                </div>

                <div style={styles.inputGroup}>
                    <label htmlFor="userTel" style={styles.label}>전화번호</label>
                    <input
                        type="tel"
                        id="userTel"
                        name="userTel"
                        style={styles.input}
                        value={userData.userTel}
                        onChange={handleChange}
                    />
                </div>

                <div style={styles.inputGroup}>
                    <label htmlFor="userAge" style={styles.label}>나이</label>
                    <input
                        type="number"
                        id="userAge"
                        name="userAge"
                        style={styles.input}
                        value={userData.userAge}
                        onChange={handleChange}
                    />
                </div>

                <button type="submit" style={styles.button} disabled={!isFormValid()}>회원가입</button>
            </form>
        </div>
    );
}

export default RegisterPage;

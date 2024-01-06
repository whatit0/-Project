import React, { useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useLocation } from 'react-router-dom';

function DeleteAccount() {
    const navigate = useNavigate();
    const location = useLocation();
    const userId = location.state?.userId;

    useEffect(() => {
        const confirmDelete = async () => {
            if (window.confirm('정말로 계정을 삭제하시겠습니까?')) {
                try {
                    const response = await axios.post("http://localhost:8080/public/user/delete", null, {
                        params: {
                            userid: userId
                        }
                    });
                    console.log(response.data);
                    alert('계정이 성공적으로 삭제되었습니다.');
                    localStorage.removeItem('accessToken');
                    localStorage.removeItem('expiresIn');
                    navigate('/');
                } catch (error) {
                    console.error('계정 삭제 실패', error);
                    alert('계정 삭제 실패: ' + error.message);
                }
            }
        };

        confirmDelete();
    }, [userId, navigate]);

    return (
        <div>
            <p>계정 삭제 처리 중...</p>
        </div>
    );
}

export default DeleteAccount;

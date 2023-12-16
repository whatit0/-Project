import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

function Home() {
  const navigate = useNavigate();
  const [responseData, setResponseData] = useState(null);

  const fetchDataFromDjango = async () => {
    try {
      const response = await axios.get('http://localhost:8000/ex/', {
        withCredentials: true,
      });
      console.log(response.data.rent_predictions);
      console.log(response.data.return_predictions);
  
      // 직접 상태를 전달하도록 수정
      navigate('/PredictionResult', {
        state: {
          rent_predictions: response.data.rent_predictions,
          return_predictions: response.data.return_predictions,
        },
      });
    } catch (error) {
      console.error('Error fetching data from Django:', error);
    }
  };
  

  return (
    <>
      <Link to="/loginPage">로그인</Link>
      <Link to="/registerPage">회원가입</Link>
      <button onClick={fetchDataFromDjango}>Django에서 데이터 가져오기</button>
    </>
  );
}

export default Home;

import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

function Home() {
  const navigate = useNavigate();
  const [responseData, setResponseData] = useState(null);

  const fetchDataFromDjango = async () => {
    try {
      const response = await axios.get('http://localhost:80/ex/',{
        withCredentials: true,  
    });
    console.log(response.data.rent_predictions);
    console.log(response.data.return_predictions);
      setResponseData(response.data);

      // 여기서 데이터를 가지고 페이지 전환 또는 다음 작업 수행
      navigate('/PredictionResult', { state: { responseData: response.data } });
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

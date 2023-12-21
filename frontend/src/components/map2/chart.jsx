// BikeChart.jsx 파일
import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import axios from 'axios';

const BikeChart = () => {
  const [chartData, setChartData] = useState({ labels: [], data: [] });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:80/chart'); // 백엔드 API 엔드포인트
        setChartData(response.data); // 백엔드에서 받은 데이터 설정
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  const data = {
    labels: chartData.labels,
    datasets: [
      {
        label: 'Bike Usage',
        data: chartData.data,
        // 그래프 스타일 등 설정 가능
      },
    ],
  };

  return (
    <div>
      <h2>Bike Usage Chart</h2>
      <Line data={data} />
    </div>
  );
};

export default BikeChart;

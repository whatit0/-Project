import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Chart from 'chart.js/auto';
import { Line } from "react-chartjs-2";

const BikeChart = () => {
  const [chartData, setChartData] = useState({ labels: [], data: [] });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [chart, setChart] = useState(null); // Chart 객체 추가

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:80/chart');
        setChartData(response.data);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
        setError('Error fetching data');
        setIsLoading(false);
      }
    };

    fetchData();

    // Cleanup 함수를 사용하여 컴포넌트 언마운트 시 Chart 객체 파괴
    return () => {
      if (chart) {
        chart.destroy();
      }
    };
  }, [chart]); // chart 의존성 추가

  useEffect(() => {
    if (chartData.labels.length > 0 && chartData.data.length > 0) {
      const ctx = document.getElementById('bikeChart');
      if (ctx) {
        if (chart) { // 이전 차트가 있는 경우에만 파괴
          chart.destroy();
        }
        
        const newChart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: chartData.labels,
            datasets: [
              {
                label:'잔여대수',
                data: chartData.data,
                backgroundColor: 'hotpink', // 핫 핑크 색상 설정
                borderColor: 'hotpink', // 테두리 색상 설정
                // 추가적인 차트 설정 가능
              },
            ],
          },
          options: {
            plugins: {
              tooltip: {
                callbacks: {
                  label: function (tooltipItem) {
                    // y축에 '개'라는 단어를 추가하여 정수 데이터를 표시
                    return tooltipItem.formattedValue + '대';
                  },
                },
              },
              legend:{
                display:false,
              },
            },
            scales: {
              y: {
                ticks: {
                  precision: 0,
                  callback: function (value) {
                    // y축 라벨에 '개'를 추가하여 반환합니다.
                    return value + '개';
                  },
                },
              },
            },
          },
        });
  
        setChart(newChart);
      }
    }
  }, [chartData]);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <h2 class='white'>Bike Usage Chart</h2>
      <canvas id="bikeChart"></canvas>
    </div>
  );
};

export default BikeChart;

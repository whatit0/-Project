import React from 'react';

const PredictionResult = ({ rent_predictions, return_predictions }) => {
  return (
    <div>
      <h1>예측 결과</h1>
      <p>대여 예측: {rent_predictions && rent_predictions.length > 0 ? rent_predictions[0] : '값이 없음'}</p>
      <p>반납 예측: {return_predictions && return_predictions.length > 0 ? return_predictions[0] : '값이 없음'}</p>
    </div>
  );
}

export default PredictionResult;

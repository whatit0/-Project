// App.js
import React from 'react';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import TopMember from "./components/member/member";
import Home from "./components/main";
import LoginPage from "./components/member/LoginPage";
import RegisterPage from "./components/member/RegisterPage";
import PredictionResult from "./components/datatest/test";


function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/loginPage" element={<LoginPage />}/>
                <Route path="/registerPage" element={<RegisterPage />}/>
                <Route path="/PredictionResult" element={<PredictionResult />}/>

            </Routes>
        </BrowserRouter>
    );

}

export default App;

// App.js
import React from 'react';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import TopMember from "./components/member/member";
import Home from "./components/main";
import LoginPage from "./components/member/loginPage";


function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/loginPage" element={<LoginPage />}/>
            </Routes>
        </BrowserRouter>
    );

}

export default App;

// App.js
import React from 'react';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./components/main";
import LoginPage from "./components/member/LoginPage";
import RegisterPage from "./components/member/RegisterPage";
import BoardList from "./components/member/BoardList";
import LoginPageTest from "./components/member/LoginPageTest";
import RoomList from "./components/chat/RoomList";
import RoomDetail from "./components/chat/RoomDetail";


function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/loginPage" element={<LoginPage />}/>
                <Route path="/loginPageTest" element={<LoginPageTest />}/>
                <Route path="/registerPage" element={<RegisterPage />}/>
                <Route path="/boardList" element={<BoardList />}/>
                <Route path="/chatList" element={<RoomList />}/>
                <Route path="/chat/room/enter/:roomId" element={<RoomDetail />}/>
            </Routes>
        </BrowserRouter>
    );

}

export default App;

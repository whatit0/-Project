// App.js
import React from 'react';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import BoardDetail from "./components/board/BoardDetail";
import BoardList from "./components/board/BoardList";
import BoardUpdate from "./components/board/BoardUpdate";
import BoardWrite from "./components/board/BoardWrite";
import RoomDetail from "./components/chat/RoomDetail";
import RoomList from "./components/chat/RoomList";
import Header from './components/common/Header';
import Home from "./components/main";
import LoginPage from "./components/member/LoginPage";
import LoginPageTest from "./components/member/LoginPageTest";
import RegisterPage from "./components/member/RegisterPage";


function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/header" element={<Header />}/>
                <Route path="/loginPage" element={<LoginPage />}/>
                <Route path="/loginPageTest" element={<LoginPageTest />}/>
                <Route path="/registerPage" element={<RegisterPage />}/>
                <Route path="/boardList" element={<BoardList />}/>
                <Route path="/boardDetail" element={<BoardDetail />}/>
                <Route path="/chatList" element={<RoomList />}/>
                <Route path="/chat/room/enter/:roomId" element={<RoomDetail />}/>
                <Route path="/boardwrite" element={<BoardWrite />}/>
                <Route path="/boardUpdate" element={<BoardUpdate />}/>
            </Routes>
        </BrowserRouter>
    );

}

export default App;

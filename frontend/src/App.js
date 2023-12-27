// App.js
import React from 'react';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import LoginPage from "./components/member/LoginPage";
import RegisterPage from "./components/member/RegisterPage";
import BoardList from "./components/board/BoardList";
import LoginPageTest from "./components/member/LoginPageTest";
import RoomList from "./components/chat/RoomList";
import RoomDetail from "./components/chat/RoomDetail";
import BoardWrite from "./components/board/BoardWrite";
import BoardDetail from "./components/board/BoardDetail";
import BoardUpdate from "./components/board/BoardUpdate";
import Map from "./components/map/Map";
import Mypage from "./components/mypage/Mypage";
import Report from "./components/map/Report";


function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Map/>}/>
                <Route path="/loginPage" element={<LoginPage />}/>
                <Route path="/loginPageTest" element={<LoginPageTest />}/>
                <Route path="/registerPage" element={<RegisterPage />}/>
                <Route path="/boardList" element={<BoardList />}/>
                <Route path="/boardDetail" element={<BoardDetail />}/>
                <Route path="/chatList" element={<RoomList />}/>
                <Route path="/chat/room/enter/:roomId" element={<RoomDetail />}/>
                <Route path="/boardwrite" element={<BoardWrite />}/>
                <Route path="/boardUpdate" element={<BoardUpdate />}/>
                <Route path="/mypage" element={<Mypage />}/>
                <Route path="/report" element={<Report />}/>
            </Routes>
        </BrowserRouter>
    );

}

export default App;

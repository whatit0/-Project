// App.js
import React from 'react';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import RoomDetail from "./components/chat/RoomDetail";
import RoomList from "./components/chat/RoomList";
import Home from "./components/main";
import Map from "./components/map2/Map";
import LoginPage from "./components/member/LoginPage";
import RegisterPage from "./components/member/RegisterPage";


function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/map" element={<Map />} />
                <Route path="/loginPage" element={<LoginPage />}/>
                <Route path="/registerPage" element={<RegisterPage />}/>
                <Route path="/chatList" element={<RoomList />}/>
                <Route path="/chat/room/enter/:roomId" element={<RoomDetail />}/>
            </Routes>
        </BrowserRouter>
    );

}

export default App;

// App.js
import React from 'react';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Footer from './components/common/Footer';
import Header from './components/common/Header';
import Map from './components/map2/Map';



function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Map />} />
                <Route path="/header" element={<Header />} />
                <Route path="/footer" element={<Footer />} />
            </Routes>
        </BrowserRouter>
    );

}

export default App;
// App.js
import React from 'react';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Map from './components/map2/Map';



function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Map />} />
            </Routes>
        </BrowserRouter>
    );

}

export default App;
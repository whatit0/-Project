let express = require("express");
let axios = require("axios");
const path = require('path');

let app = express()
let port = process.env.PORT || 8087;

app.use(express.static("html"));
app.use(express.static(path.join(__dirname, '../style')));
app.use(express.static(path.join(__dirname, '../js')));

app.listen(port, function () {
    console.log("HTML 서버 시작")
})
// http://openapi.seoul.go.kr:8088/704270597679656a35366a6f776e72/xml/bikeStationMaster/1/5/
// http://openapi.seoul.go.kr:8088/6c4c52594d79656a38317a4b684554/json/tbCycleStationInfo/1/5/
// http://openapi.seoul.go.kr:8088/537676746c79656a39306c4b4a5a64/json/bikeList/1/5/
app.get("/map_list", async (req, res) => {
    try {
        // 페이지네이션을 위한 변수
        const itemsPerPage = 1000;  // 페이지당 아이템 수
        const totalItems = 3000;  // 전체 아이템 수
        let allData = [];

        // 페이지별로 요청하여 데이터를 합침
        for (let page = 1; page <= Math.ceil(totalItems / itemsPerPage); page++) {
            let response = await axios.get(`http://openapi.seoul.go.kr:8088/456852427579656a313035727966656c/json/bikeList/${(page - 1) * itemsPerPage + 1}/${page * itemsPerPage}`);
            allData = allData.concat(response.data.rentBikeStatus.row);
        }

        res.setHeader("Access-Control-Allow-Origin", "*");
        res.json({ rentBikeStatus: { row: allData } });
    } catch (error) {
        console.error(error);
        res.status(500).send("내부 서버 오류");
    }
});

app.get("/search", async (req, res) => {
    try {
        let allData = [];
        const itemsPerPage = 1000;  // 페이지당 아이템 수
        const totalItems = 3000;  // 전체 아이템 수
        const searchName = req.query.searchName; // 대여소명을 가져옴
        
        // 페이지별로 요청하여 데이터를 합침
        for (let page = 1; page <= Math.ceil(totalItems / itemsPerPage); page++) {
            let response = await axios.get(`http://openapi.seoul.go.kr:8088/456852427579656a313035727966656c/json/bikeList/${(page - 1) * itemsPerPage + 1}/${page * itemsPerPage}`);
            allData = allData.concat(response.data.rentBikeStatus.row);
        }
        // 검색어와 일치하는 대여소 필터링
        const searchResults = allData.filter(station => station.stationName.includes(searchName));

        res.setHeader("Access-Control-Allow-Origin", "*");
        res.json({ searchResults });
    } catch (error) {
        console.error(error);
        res.status(500).send("내부 서버 오류");
    }
});
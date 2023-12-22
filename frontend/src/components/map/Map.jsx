import axios from 'axios';
import React, { useEffect, useState } from 'react';
import {Link, useNavigate} from 'react-router-dom';
import "../style/base.css";
import "../style/bootstrap.css";
import "../style/main.css";
import "../style/rome.css";

function Map() {
    const { naver } = window;
    const [markerData, setMarkerData] = useState([]);
    const [map, setMap] = useState(null);
    const [searchResults, setSearchResults] = useState([]);
    const [searchValue, setSearchValue] = useState("");
    const [selectedStationId, setSelectedStationId] = useState(null);
    const [myLocationMarker, setMyLocationMarker] = useState(null);
    const [parkingBikeTotCnt, setParkingBikeTotCnt] = useState(null);
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const token1 = localStorage.getItem('accessToken');
    const token2 = localStorage.getItem('expiresIn');
    const navigate = useNavigate();

    useEffect(() => {

        if (token1 && token2) {
            // 토큰 유효성 검증 로직 (옵션)
            setIsLoggedIn(true);
        }
    }, []);

    const includedIds = [
        'ST-814', 'ST-1181', 'ST-1879', 'ST-1245', 'ST-799', 'ST-1703', 'ST-1680', 'ST-1575', 'ST-1885',
        'ST-777', 'ST-1559', 'ST-1247', 'ST-1897', 'ST-1895', 'ST-960', 'ST-1880', 'ST-966', 'ST-1574', 'ST-1896',
        'ST-953', 'ST-797', 'ST-804', 'ST-1407', 'ST-1560', 'ST-818', 'ST-795', 'ST-787', 'ST-791', 'ST-1888',
        'ST-1578', 'ST-1892', 'ST-812', 'ST-1679', 'ST-807', 'ST-802', 'ST-1364', 'ST-1184', 'ST-1433', 'ST-822',
        'ST-1171', 'ST-1884', 'ST-784', 'ST-798', 'ST-816', 'ST-782', 'ST-794', 'ST-820', 'ST-810', 'ST-1887',
        'ST-821', 'ST-1571', 'ST-1566', 'ST-796', 'ST-1704', 'ST-1365', 'ST-1178', 'ST-956', 'ST-1893', 'ST-1889',
        'ST-937', 'ST-1886', 'ST-790', 'ST-1174', 'ST-783', 'ST-1576', 'ST-811', 'ST-1248', 'ST-1573', 'ST-809',
        'ST-786', 'ST-793', 'ST-959', 'ST-1246', 'ST-954', 'ST-792', 'ST-779', 'ST-1564', 'ST-815', 'ST-963',
        'ST-1177', 'ST-1366', 'ST-1172', 'ST-1180', 'ST-803', 'ST-958', 'ST-806', 'ST-1882', 'ST-1563', 'ST-1894',
        'ST-1182', 'ST-1562', 'ST-1891', 'ST-957', 'ST-1565', 'ST-1185', 'ST-962', 'ST-1179', 'ST-1568', 'ST-1881',
        'ST-1561', 'ST-801', 'ST-817', 'ST-961', 'ST-778',
    ];


    // ----------------------------------------------------------------------

    // ----------------------------------------------------------------------
    const addMarkerData = (station) => {
        let markerInfo = {
            stationId: station.stationId,
            stationName: station.stationName,
            parkingBikeTotCnt: station.parkingBikeTotCnt,
        };

        // Clear existing content
        const mapDataInfo = document.getElementById('map_data_cont');
        mapDataInfo.textContent = '';

        // Append the new marker info
        const infoDiv = document.createElement('div');
        infoDiv.textContent = markerInfo.stationName;
        infoDiv.classList.add('bicycle_name');
        mapDataInfo.appendChild(infoDiv);

        const mapDataInfo2 = document.getElementById('map_data_cont2');
        mapDataInfo2.textContent = '';

        const infoDiv2 = document.createElement('div');
        infoDiv2.innerHTML = `<p class="bicycle_count shadow-sm">현재 따릉이 잔여 대수 <span>${markerInfo.parkingBikeTotCnt}대</span></p>`;
        mapDataInfo2.appendChild(infoDiv2);

        console.log('Clicked Station Info:', markerInfo);
        setSelectedStationId(markerInfo.stationId);
        setParkingBikeTotCnt(markerInfo.parkingBikeTotCnt);
    };


    const getLocation = async () => {
        let XY = { lat: 0, lng: 0 };
        if (navigator.geolocation) {
            try {
                const position = await new Promise((resolve) => {
                    navigator.geolocation.getCurrentPosition((pos) => resolve(pos));
                });
                XY.lat = position.coords.latitude;
                XY.lng = position.coords.longitude;
            } catch (error) {
                console.error(error);
            }
        }
        return XY;
    };

    const moveToMyLocation = async () => {
        const location = await getLocation();
        if (location && map) {
            const myLocation = new naver.maps.LatLng(location.lat, location.lng);
            map.setCenter(myLocation);

            // 이전 마커가 있으면 제거
            if (myLocationMarker) {
                myLocationMarker.setMap(null);
            }

            // 새로운 마커를 생성하고 지도에 추가
            const newMarker = new naver.maps.Marker({
                position: myLocation,
                map: map,
                icon: {
                    content: [
                        '<span class="material-icons red fs45">location_on</span>',
                    ].join(''),
                    size: new naver.maps.Size(38, 58),
                    anchor: new naver.maps.Point(19, 58),
                },
            });

            // 새로운 마커를 상태로 업데이트
            setMyLocationMarker(newMarker);
        }
    };


    const moveToGangnam = () => {
        if (map) {
            const gangLat = 37.49599969478604;
            const gangLng = 127.03292823149238;
            const zoomLevel = 15;
            const gangLocation = new naver.maps.LatLng(gangLat, gangLng);
            map.setCenter(gangLocation);
            map.setZoom(zoomLevel);
        }
    };

    const handleSearchClick = (e) => {
        e.preventDefault();
        const searchTerm = e.target.elements.searchValue.value;
        if (searchTerm.trim() !== "") {
            // 검색 결과 필터링
            const results = markerData.filter((station) =>
                station.stationName.includes(searchTerm) && includedIds.includes(station.stationId)
            );
            setSearchResults(results);
            // 첫 번째 검색 결과에 대해 addMarkerData 함수 호출
            if (results.length > 0) {
                addMarkerData(results[0]);
            } else {
                alert('검색 결과가 없습니다.');
            }
        } else {
            setSearchResults([]); // 검색어가 비어있는 경우 결과 초기화
        }
    };

    const handleSearchResultClick = (result) => {
        // 클릭한 검색 결과에 대한 처리 수행
        addMarkerData(result);

        // map_data_search 숨기기
        // 아래처럼 숨김 처리를 하거나, CSS를 통해 display: none; 처리도 가능합니다.
        const mapDataSearch = document.querySelector('.map_data_search');
        if (mapDataSearch) {
            mapDataSearch.style.display = 'none';
        }
        setSearchResults([]);
    };

    const handlePredictionSubmit = async (e) => {
        e.preventDefault();

        const formData = new FormData(e.target);
        const date = formData.get('reservationDate');
        const time = formData.get('reservationTime');

        try {
            const response = await axios.get('http://localhost:80/ex', {
                params: {
                    date,
                    time,
                    stationId: selectedStationId,
                    parkingBike:parkingBikeTotCnt,

                },
            });


            const rent_predictions = response.data.rent_predictions;
            const return_predictions = response.data.return_predictions;
            const leftbike = response.data.leftbike;

            const rentElement = document.querySelector('.rental_num');
            if (rentElement) {
                rentElement.textContent = rent_predictions.length > 0 ? rent_predictions[0] : '0';
            }

            const returnElement = document.querySelector('.return_num');
            if (returnElement) {
                returnElement.textContent = return_predictions.length > 0 ? return_predictions[0] : '0';
            }

            const rentalElement = document.querySelector('.count');
            if (rentalElement) {
                rentalElement.textContent = leftbike;
            }

            console.log(rent_predictions);
            console.log(time);

        } catch (error) {
            console.error('Error fetching data from Django:', error);
        }

    };

    useEffect(() => {
        const fetchData = async () => {
            try {
                const itemsPerPage = 1000;
                const totalItems = 3000;
                let allData = [];

                for (let page = 1; page <= Math.ceil(totalItems / itemsPerPage); page++) {
                    let response = await axios.get(`http://openapi.seoul.go.kr:8088/456852427579656a313035727966656c/json/bikeList/${(page - 1) * itemsPerPage + 1}/${page * itemsPerPage}`);
                    allData = allData.concat(response.data.rentBikeStatus.row);
                }

                setMarkerData(allData);
            } catch (error) {
                console.error(error);
            }
        };

        fetchData();
    }, []);

    useEffect(() => {
        if (markerData.length > 0 && !map) {
            const initMap = async () => {
                try {
                    //const XY = await getLocation();
                    const mapOptions = {
                        scaleControl: false,
                        logoControl: false,
                        mapDataControl: false,
                        zoomControl: true,
                        minZoom: 6,
                        center: new naver.maps.LatLng(37.49599969478604, 127.03292823149238),
                        zoom: 15,

                        mapTypeControl: true,
                        mapTypeControlOptions: {
                            style: naver.maps.MapTypeControlStyle.BUTTON,
                            position: naver.maps.Position.BOTTOM_RIGHT,
                        },
                        zoomControlOptions: {
                            style: naver.maps.ZoomControlStyle.SMALL,
                            position: naver.maps.Position.BOTTOM_RIGHT,
                        },
                        logoControlOptions: {
                            position: naver.maps.Position.BOTTOM_LEFT,
                        },
                    };
                    const newMap = new naver.maps.Map('map', mapOptions);
                    setMap(newMap);

                    const markers = [];
                    let markerCount = 0;

                    markerData.forEach((station) => {
                        if (includedIds.includes(station.stationId)) {
                            const marker = new naver.maps.Marker({
                                position: new naver.maps.LatLng(station.stationLatitude, station.stationLongitude),
                                map: newMap,
                                icon: {
                                    content: [
                                        '<div class="map_marker main_color"> ',
                                        '<span class="ico _icon"><span class="material-symbols-rounded marker_icon white">pedal_bike</span></span>',
                                        '<span class="shd"></span>',
                                        '</div>',
                                    ].join(''),
                                    size: new naver.maps.Size(38, 58),
                                    anchor: new naver.maps.Point(19, 58),
                                },
                            });

                            markers.push(marker);

                            naver.maps.Event.addListener(marker, 'click', () => {
                                document.getElementById('map_data_info').style.display = 'block';
                                addMarkerData(station);
                                //updateMapInfo();
                            });

                            markerCount++;
                        }
                    });

                    console.log('마커 개수:' + markerCount);
                } catch (error) {
                    console.error(error);
                }
            };

            initMap();
        }
    }, [markerData, map]);

    const handleLogout = () => {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('expiresIn');
        setIsLoggedIn(false);

    };

    const handleMypage = () =>{
        window.location.href='/mypage'
    }

    return (
        <div id="map">
            <div id="map_info">
                <div id="map_info_left">
                    <div className="left_head">
                        <Link to="/" className="left_menu left_menu01">
                            <div className="flex_center">
                                <span className="material-symbols-rounded">map</span>
                                <p className="menu_name">홈</p>
                            </div>
                        </Link>
                        <Link to="/chatList" className="left_menu left_menu02">
                            <div className="flex_center">
                                <span className="material-symbols-rounded">sms</span>
                                <p className="menu_name">채팅</p>
                            </div>
                        </Link>
                        <Link to="/boardList" className="left_menu left_menu03">
                            <div className="flex_center">
                                <span className="material-symbols-rounded">group</span>
                                <p className="menu_name">커뮤니티</p>
                            </div>
                        </Link>
                        <Link to="" className="left_menu left_menu04">
                            <div className="flex_center">
                                <span className="material-symbols-rounded">description</span>
                                <p className="menu_name">공지사항</p>
                            </div>
                        </Link>
                        <div>
                            {isLoggedIn ? (
                                <button onClick={handleMypage} className="left_menu left_menu05">
                                    <div className="flex_center">
                                        <span className="material-symbols-rounded">home</span>
                                        <p className="menu_name">마이페이지</p>
                                    </div>
                                </button>
                            ) : (
                                <button onClick={() => window.location.href = '/loginPage' }className="left_menu left_menu05">
                                    <div className="flex_center">
                                        <span className="material-symbols-rounded">home</span>
                                        <p className="menu_name">로그인</p>
                                    </div>
                                </button>
                            )}
                        </div>
                        <Link to="" className="left_menu left_menu05">

                        </Link>
                    </div>
                    <div id="map_data_info">
                        <div className="map_data_top">
                            <div id="search">
                                <form onSubmit={handleSearchClick}>
                                    <label htmlFor="ser_title" className="away">
                                        검색어 입력
                                    </label>
                                    <input
                                        type="hidden"
                                        name="searchName"
                                        value="model"
                                    />
                                    <input
                                        type="text"
                                        className="search_text"
                                        placeholder="대여소명을 입력해주세요"
                                        name="searchValue"
                                        id="ser_title"
                                        value={searchValue}
                                        onChange={(e) => setSearchValue(e.target.value)}
                                    />
                                    <button type="submit" className="search_btn">
                                        <span className="material-symbols-rounded fs25">
                                            search
                                        </span>
                                    </button>
                                </form>
                            </div>
                            <div className="bicycle_info flex">
                                <div className="wd25"></div>
                                <div id="map_data_cont"></div>
                                <span className="material-symbols-rounded close_btn">close</span>
                            </div>
                        </div>
                        {/* 검색 결과를 동적으로 렌더링 */}
                        {searchResults.length > 0 && (
                            <div className="map_data_search">
                                <div className="search-results">
                                    <p className="map_data_title">검색 결과 ({searchResults.length}건)</p>
                                    <ul>
                                        {searchResults.map((result) => (
                                            <li key={result.stationId} onClick={() => handleSearchResultClick(result)}>
                                                {result.stationName}
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            </div>
                        )}
                        <div id="map_data_cont2"></div>
                        <div className="map_data_bottom">
                            <div className="date_time">
                                <p className="map_data_title">잔여 대수 예측하기</p>
                                <form onSubmit={handlePredictionSubmit} id="pred_form">
                                    <div className="datepicker date input-group p-0 shadow-sm">
                                        <input
                                            type="text"
                                            placeholder="날짜를 선택해주세요"
                                            className="form-control py-3 px-3"
                                            id="reservationDate"
                                            name="reservationDate"
                                        />
                                        <div className="input-group-append">
                                            <span className="material-symbols-rounded fs20 fw400 dgreen input-group-text px-3">event_available</span>
                                        </div>
                                    </div>
                                    <div className="time">
                                        <div className="form-group">
                                            <div className="input-group time shadow-sm" id="timepicker">
                                                <input
                                                    type="text"
                                                    className="form-control py-3 px-3"
                                                    placeholder="시간을 선택해주세요"
                                                    name="reservationTime"
                                                />
                                                <span className="input-group-append">
                                                    <span className="material-symbols-rounded fs20 fw400 dgreen input-group-text px-3">schedule</span>
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                    <button type="submit" id="pred_btn">예측하기</button>
                                </form>
                                <div id="result_cont">
                                    <p className="map_data_title">잔여 대수 예측결과</p>
                                    <div className="result_data flex">
                                        <div className="return_data">
                                            <p className="flex2">
                                                <span className="material-symbols-rounded fs25 fw400 wd22 red">arrow_drop_up</span>
                                                <span className="red">예상 반납건수</span>
                                            </p>
                                            <p><span className="return_num">0</span>건</p>
                                        </div>
                                        <div className="rental_data">
                                            <p className="flex2">
                                                <span className="material-symbols-rounded fs25 fw400 wd22 blue">arrow_drop_down</span>
                                                <span className="blue">예상 대여건수</span>
                                            </p>
                                            <p><span className="rental_num">0</span>건</p>
                                        </div>
                                    </div>
                                    <div className="result_count flex">
                                        <p>따릉이 잔여 대수 예측 결과</p>
                                        <p><span className="count">0</span>대</p>
                                    </div>
                                </div>

                            </div>
                        </div>
                    </div>
                </div>

                <div id="map_info_right">
                    <div className="user_icon icon_box">
                        {isLoggedIn ? (
                            <button onClick={handleLogout} className="left_menu left_menu05">
                                <div className="flex_center">
                                    <span className="material-icons">account_circle</span>
                                </div>
                            </button>
                        ) : (
                            <button onClick={() => window.location.href = '/loginPage' }className="left_menu left_menu05">
                                <div className="flex_center">
                                    <span className="material-icons">account_circle</span>
                                </div>
                            </button>
                        )}
                    </div>
                    <div className="gps_icon icon_box" onClick={moveToMyLocation}>
                        <span className="material-icons">gps_fixed</span>
                    </div>
                    <div className="bicycle_icon icon_box" onClick={moveToGangnam}>
                        <span className="material-symbols-rounded fs25 fw500">directions_bike</span>
                    </div>
                </div>
            </div>
        </div>
    );


}

export default Map;
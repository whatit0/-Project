import React from "react";


function Edituser(){

    return(
        <>
            <div className="mypage-content">
                <h1 className="content-title">개인 정보 수정</h1>
                <form className="info-form">
                    <label className="form-label">
                        <span>아이디</span>
                        <input type="text" className="form-input" readOnly />
                    </label>
                    <label className="form-label">
                        <span>비밀번호</span>
                        <input type="password" className="form-input" placeholder="현재 비밀번호를 입력하세요" />
                    </label>
                    <label className="form-label">
                        <span>새 비밀번호</span>
                        <input type="password" className="form-input" placeholder="새 비밀번호를 입력하세요" />
                    </label>
                    <label className="form-label">
                        <span>새 비밀번호 확인</span>
                        <input type="password" className="form-input" placeholder="새 비밀번호를 다시 입력하세요" />
                    </label>
                    <label className="form-label">
                        <span>이메일</span>
                        <input type="email" className="form-input" placeholder="이메일을 입력하세요" />
                    </label>
                    <div style={{width : "100%", textAlign: "center"}}><button type="submit" className="form-submit">변경사항 저장</button></div>
                </form>
            </div>
        </>
    )

}


export default Edituser;
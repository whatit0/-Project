import React from "react";


function Edituser(){

    return(
        <>
            <div className="mypage-content">
                <h1 className="content-title">개인 정보 수정</h1>
                <form className="info-form">
                    <label className="form-label">
                        아이디
                        <input type="text" className="form-input" readOnly />
                    </label>
                    <label className="form-label">
                        비밀번호
                        <input type="password" className="form-input" placeholder="현재 비밀번호를 입력하세요" />
                    </label>
                    <label className="form-label">
                        새 비밀번호
                        <input type="password" className="form-input" placeholder="새 비밀번호를 입력하세요" />
                    </label>
                    <label className="form-label">
                        새 비밀번호 확인
                        <input type="password" className="form-input" placeholder="새 비밀번호를 다시 입력하세요" />
                    </label>
                    <label className="form-label">
                        이메일
                        <input type="email" className="form-input" placeholder="이메일을 입력하세요" />
                    </label>
                    <button type="submit" className="form-submit">변경사항 저장</button>
                </form>
            </div>
        </>
    )

}


export default Edituser;
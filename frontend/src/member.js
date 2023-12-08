import logo from './logo.svg';
import './App.css';


function TopMember (index){
  let output;
  if(index===1){
    output = "로그인";
  }else if(index===2){
    output = "회원가입";
  }
  return(
      <div className="Login">
        <a>{output}</a>
      </div>
  )
}

export default TopMember;

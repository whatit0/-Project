import React from 'react';


function TopMember (props){
  let output;
  if(props.name==='login'){
    output = "로그인";
  }else if(props.name==='register'){
    output = "회원가입";
  }
  return(
      <span>
        <a href={props.name}>{output}</a>
      </span>
  )
}

export default TopMember;

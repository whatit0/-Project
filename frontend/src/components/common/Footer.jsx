import React from 'react';
import { Link } from 'react-router-dom';

function Footer() {
    return (
        <div id='footer'>
            <div className="footer_wrap">
                <div id="f_top">COPYRIGHT (C) CORP. ALL RIGHTS RESERVED</div>
                <div id="f_bottom">
                    <Link to="/" className='flex'>
                        <div className='bg_square'><span className="material-icons fs15 white">play_arrow</span></div>
                        <span className="material-icons fs30 li-gray">email</span>
                    </Link>
                </div>
            </div>
        </div>
    );
}

export default Footer;
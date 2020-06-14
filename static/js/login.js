'use strict'

//header函数
var SStd = document.getElementById('s-std');
var SAd = document.getElementById('s-ad');
    SStd.onclick = function () {

        SAd.style.textDecoration = 'none';
        SAd.style.color = '#a0a0a0';
        SStd.style.color = '#ffab08';
        SStd.style.textDecoration = 'underline';
        return 's-Std';

    };
    SAd.onclick = function () {

        SStd.style.color = '#a0a0a0';
        SStd.style.textDecoration = 'none';
        SAd.style.color = '#ffab08';
        SAd.style.textDecoration = 'underline';
        return 's-ad';
    };



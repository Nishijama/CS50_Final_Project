//---------------
//requests/pages settup
var type = 'requests';
document.getElementById("reqButton").style.backgroundColor = "#00A9F4";

document.getElementById('reqButton').addEventListener('click', function(){
    document.getElementById("reqButton").style.backgroundColor = "#00A9F4";
    document.getElementById("pagesButton").style.backgroundColor = "#051C2C";
    // document.getElementById("prcImage").src="static/requestChart.png";
    type = 'requests';
})

document.getElementById('pagesButton').addEventListener('click', function() {
    document.getElementById("pagesButton").style.backgroundColor = "#00A9F4";
    document.getElementById("reqButton").style.backgroundColor = "#051C2C";
    // document.getElementById("prcImage").src="static/pagesChart.png";
    type = 'pages'
})

//-------------
// //table vs chart settup

//----------
//Pop-up setup


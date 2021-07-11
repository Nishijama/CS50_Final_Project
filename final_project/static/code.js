

//default setup
var type = 'requests';
document.getElementById("reqButton").style.backgroundColor = "#00A9F4";

var state = 'chart';
document.getElementById("table/chart").innerHTML = 'Table view';

document.getElementById("prcImage").src="static/requestChart.png";

var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
var d = new Date();
var n = d.getMonth();
document.getElementById("date").innerHTML = months[n];

//---------------
//date settup

document.getElementById('prevMonth').addEventListener('click', function(){
    n -= 1
    if (n < 0) {
        n = 11;
    }

    document.getElementById("date").innerHTML = months[n]
})

document.getElementById('nextMonth').addEventListener('click', function(){
    n += 1
    if (n > 11) {
        n = 0;
    }
    document.getElementById("date").innerHTML =  months[n];
})

//---------------
//requests/pages settup

document.getElementById('reqButton').addEventListener('click', function(){
    document.getElementById("reqButton").style.backgroundColor = "#00A9F4";
    document.getElementById("pagesButton").style.backgroundColor = "#051C2C";

    if (state == 'chart'){
        document.getElementById("prcImage").src="static/requestChart.png";
    }
    else if (state == 'table') {
        document.getElementById("prcImage").src="static/requestTable.png";
    }

    type = 'requests';
})

document.getElementById('pagesButton').addEventListener('click', function() {
    document.getElementById("pagesButton").style.backgroundColor = "#00A9F4";
    document.getElementById("reqButton").style.backgroundColor = "#051C2C";

    if (state == 'chart'){
        document.getElementById("prcImage").src="static/pagesChart.png";
    }
    else if (state == 'table') {
        document.getElementById("prcImage").src="static/pagesTable.png";
    }

    type = 'pages'
})

//-------------
//table vs chart settup

document.getElementById('table/chart').addEventListener('click', function() {

    if (state == 'chart'){

        document.getElementById("table/chart").innerHTML = 'Chart view';

        if (type == 'requests'){
            document.getElementById("prcImage").src="static/requestTable.png";
        }
        else if (type == 'pages') {
            document.getElementById("prcImage").src="static/pagesTable.png";
        }
        state = 'table';
    }

    else if (state == 'table') {

        document.getElementById("table/chart").innerHTML = 'Table view';

        if (type == 'requests'){
            document.getElementById("prcImage").src="static/requestChart.png";
        }
        else if (type == 'pages') {
            document.getElementById("prcImage").src="static/pagesChart.png";
        }
        state = 'chart';
    }
})

//----------
//Pop-up setup

document.getElementById('editButton').addEventListener('click', function(){
  document.querySelector('.modalBg').style.display = 'flex';
})

document.querySelector('.close').addEventListener('click', function() {
  document.querySelector('.modalBg').style.display = 'none';
})

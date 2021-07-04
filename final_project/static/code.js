var state = 'chart';
document.getElementById("table/chart").innerHTML = 'Table view';

//change text in navbar when state is changed
//if we're in the chart state:
function stateFunction () {
    if (state == 'chart') {
        document.getElementById("table/chart").innerHTML = 'Chart view';
        document.getElementById("prcImage").src="static/PRC-chart.jpg";
        state = 'table';
    return;
    }
    //if we're in the table state
    else {
        document.getElementById("table/chart").innerHTML = 'Table view';
        document.getElementById("prcImage").src="static/toDoCat.jpg";
    state = 'chart';
    return;
    }
}
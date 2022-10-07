var data;

function initGraph() {
    function initBarChart() {
        axios.get(restAPIUrl + "fullclear-stats/ZETA/").then(function (response) {
            let data = response.data;
            let labels = [];
            let ktimes = [];

            for (let i = 0; i < data.length; i++) {
                labels.push(data[i].encounter_name);
                ktimes.push(data[i].kd_sec);
            }

            let trace = [{
                x: labels,
                y: ktimes,
                name: "ZETA FC",
                type: "bar"
            }]

            Plotly.newPlot('gkt-overview-chart', trace);
        });
    }
    function init() {
        initBarChart();
    }
    init();
}

window.onload = function () {
    initGraph();
}
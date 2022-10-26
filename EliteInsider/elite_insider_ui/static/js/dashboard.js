var defaultColorLayout = {
    textColor : "#F7F6FB",
    borderColor : "#F7F6FB",
}

function initGraph() {
    function initColorLayout() {
        Chart.defaults.color = defaultColorLayout.textColor;
        Chart.defaults.borderColor = defaultColorLayout.borderColor;
    }

    function initBarChart() {
        axios.get(restAPIUrl + "fullclear-stats/ZETA/").then(function (response) {
            let data = response.data;
            let labels = []
            let ktTime = []

            for (let i = 0; i < data.length; i++) {
                labels.push(data[i].encounter_name);
                ktTime.push(data[i].kd_sec);
            }

            let ktData = [{
                label: "kill time in seconds",
                backgroundColor: "#03DAC5",
                borderColor: "#03DAC5",
                data: ktTime,
            }];

            let chartData = {
                labels: labels,
                datasets: ktData,
            };

            let config = {
                type: 'bar',
                data: chartData,
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: "Most recent fullclear",
                        },
                    },
                    scales: {
                        x: {
                          grid: {
                            display: false,
                          }
                        },
                        y: {
                          grid: {
                            display: false,
                          }
                        }
                    },
                    layout: {
                        autoPadding: true,
                    },
                }
            };

            let fcChart = new Chart(
                document.getElementById('fc-chart'),
                config
            );
        });
    }
    function init() {
        initColorLayout();
        initBarChart();
    }
    init();
}

window.onload = function () {
    initGraph();
}
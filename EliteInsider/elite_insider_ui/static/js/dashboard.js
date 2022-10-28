var defaultColorLayout = {
    textColor : "#F7F6FB",
    borderColor : "#F7F6FB",
}

var fcChart, wtChart;

function initMenuBar(){
    $("#btn-update-charts").click(function() {
        let yearweekString = $("#week-picker").val();
        yearweekString = yearweekString.replace("-W", "");

        initGraph(week=yearweekString);
    });
}

function initGraph(week=null) {
    
    let width, height, gradient;

    function initColorLayout() {
        Chart.defaults.color = defaultColorLayout.textColor;
        Chart.defaults.borderColor = defaultColorLayout.borderColor;
    }

    function getGradient(ctx, chartArea) {
        const chartWidth = chartArea.right - chartArea.left;
        const chartHeight = chartArea.bottom - chartArea.top;
        if (!gradient || width !== chartWidth || height !== chartHeight) {
        // Create the gradient because this is either the first render
        // or the size of the chart has changed
        width = chartWidth;
        height = chartHeight;
        gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
        gradient.addColorStop(0, "#03DAC5");
        gradient.addColorStop(0.5, "#02998a");
        gradient.addColorStop(1, "#03DAC5");
        }
    
        return gradient;
    }

    function initFcChart() {
        fetchUrl = restAPIUrl + "fullclear-stats/ZETA/";
        if (week) {
            fetchUrl += "?yearweek=" + week;
        }

        axios.get(fetchUrl).then(function (response) {
            let data = response.data;
            let labels = [];
            let ktTime = [];

            for (let i = 0; i < data.length; i++) {
                labels.push(data[i].encounter_name);
                ktTime.push(data[i].kill_duration_seconds);
            }

            let ktData = [{
                label: "kill time in seconds",
                backgroundColor: function(context) {
                    const chart = context.chart;
                    const {ctx, chartArea} = chart;

                    if (!chartArea) {
                    // This case happens on initial chart load
                    return;
                    }
                    return getGradient(ctx, chartArea);
                },
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
                            ticks: {
                                autoSkip: false,
                                maxRotation: 90,
                                minRotation: 90,
                            },
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

            if(fcChart) {
                fcChart.data.labels = labels;
                fcChart.data.datasets = ktData;
                fcChart.update();
            }
            else{
                fcChart = new Chart(
                    document.getElementById('fc-chart'),
                    config
                );
            }
        });
    }

    function initWingTimeChart() {
        fetchUrl = restAPIUrl + "fullclear-wing-stats/ZETA/";
        if (week) {
            fetchUrl += "?yearweek=" + week;
        }

        axios.get(fetchUrl).then(function (response) {
            let data = response.data;
            let minValue = null;
            let labels = [];
            let timeData = [];

            for (let i = 0; i < data.length; i++) {
                if(minValue == null){
                    minValue = data[i].start_time;
                }

                labels.push(data[i].wing_name);
                timeData.push([data[i].start_time, data[i].end_time]);
            }

            let dataSet = [{
                label: "Time spend in minutes",
                data:  timeData,
                borderColor: "#03DAC5",
                backgroundColor: "#03DAC5",
                barPercentage: 0.3,
            }];

            let chartData = {
                labels: labels,
                datasets: dataSet,
            };

            let config = {
                type: 'bar',
                data: chartData,
                options: {
                    responsive: true,
                    indexAxis: 'y',
                    plugins: {
                        title: {
                            display: true,
                            text: "Most recent fullclear by wing performance",
                        },
                    },
                    scales: {
                        x: {
                            min: minValue,
                            type: "time",
                            //time: {
                            //   unit: "hour",
                            //},
                            grid: {
                                display: false,
                            }
                        },
                        y: {
                          beginAtZero: true,
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

            if(wtChart) {
                wtChart.data.labels = labels;
                wtChart.data.datasets = dataSet;
                wtChart.options.scales.x.min = minValue;
                wtChart.update();
            }
            else{
                wtChart = new Chart(
                    document.getElementById('wing-time-chart'),
                    config
                );
            }
        });
    }

    function init() {
        initColorLayout();
        initFcChart();
        initWingTimeChart();
    }
    init();
}

window.onload = function () {
    initMenuBar();
    initGraph();
}
// Fetch the JSON data for graphs
d3.json("http://127.0.0.1:5000/data").then(function (data) {

    dropdown = d3.select("#locationDropdown");

    // Create a function that retrieve data for charts
    function newData(element) {
        // Variable to hold name ID value to build plots
        let condition = element.property("value");

        stateData = data[condition]

        // Set trace for timeline
        let trace_timeline = [{
            x: Object.keys(stateData.RecordCount),
            y: Object.values(stateData.RecordCount),
            fill: 'tozeroy',
            line: {
                color: '#EDC948'
            }
        }];

        // Set trace for barchart
        let trace_barchart = [{
            x: Object.keys(stateData.MedianChargedOffAmount),
            y: Object.values(stateData.MedianChargedOffAmount),
            type: "bar",
            marker: {
                color: '#EDC948',
            }
        }];

        // Set Layout for timeline
        let layout_timeline = {
            title: `Yearly trend of # of Defaulted Companies in ${dropdown.property("value")}`,
            xaxis: {
                tickvals: Object.keys(stateData.RecordCount),
            },
            yaxis: {
                title: {
                    text: '# of companies with charged off loan',
                    font: {
                        size: 12,
                        color: '#7f7f7f'
                    }
                },
            }
        };

        // Set Layout for barchart
        let layout_barchart = {
            title: `Yearly trend of AVG Charged off Amount in ${dropdown.property("value")}`,
            xaxis: {
                tickvals: Object.keys(stateData.MedianChargedOffAmount)
            },
            yaxis: {
                title: {
                    text: 'average charged off amount',
                    font: {
                        size: 12,
                        color: '#7f7f7f'
                    }
                },
            }
        };

        return ([trace_timeline, layout_timeline, trace_barchart, layout_barchart])
    };

    // Display the default charts
    function init() {
        traces = newData(dropdown)
        Plotly.newPlot('applicationsTrend', traces[0], traces[1]);
        Plotly.newPlot('amountTrend', traces[2], traces[3]);
    }

    init();

    // On change to filter, update data in charts
    dropdown.on("change", function () {
        traces = newData(dropdown)
        Plotly.react("applicationsTrend", traces[0], traces[1]);
        Plotly.react("amountTrend", traces[2], traces[3]);
    });

});







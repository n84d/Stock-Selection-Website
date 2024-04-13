document.addEventListener('DOMContentLoaded', function() {
    // Fetch chart data from the server
    fetch('/chart-data')  // Update the route to match your new route name
        .then(response => response.json())
        .then(chart_data => {
            // Modify the labels array to start at 0
            chart_data.labels = Array.from({ length: chart_data.labels.length }, (_, i) => i);
            
            // Create a line chart using Chart.js
            createLineChart(chart_data);
        })
        .catch(error => {
            console.error('Error fetching chart data:', error);
        });
});


function createLineChart(chart_data) {
    console.log('Received chart data:', chart_data);

    // Flatten the nested arrays
    var flattenedDataColumn1 = chart_data.data.column1.flat();
    var flattenedDataColumn2 = chart_data.data.column2.flat();
    var flattenedDataColumn3 = chart_data.data.column3.flat();

    var ctx = document.getElementById('myChart').getContext('2d');

    var myLineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chart_data.labels,
            datasets: [
                {
                    label: 'Top 10 Strategy',
                    data: flattenedDataColumn1,
                    borderColor: 'rgb(162, 213, 255)',
                    borderWidth: 3,
                    fill: false,
                },
                {
                    label: 'Threshold Strategy',
                    data: flattenedDataColumn2,
                    borderColor: 'rgb(35, 52, 83)',
                    borderWidth: 3,
                    fill: false,
                },
                {
                    label: 'SPY',
                    data: flattenedDataColumn3,
                    borderColor: 'rgb(218, 218, 218)',
                    borderWidth: 3,
                    fill: false,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
        },
    });
}

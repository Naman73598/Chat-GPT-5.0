fetch('../data.json')
    .then(response => response.json())
    .then(data => {
        const chartData = {
            labels: data.map(d => d.id),
            datasets: [{
                label: 'Value',
                data: data.map(d => d.accuracy),
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        };
        const chartConfig = {
            type: 'line',
            data: chartData,
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        };
        const chart = new Chart(document.getElementById('chart'), chartConfig);
    });

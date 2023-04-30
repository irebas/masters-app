const ctx = document.getElementById('myChart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [{% for label in labels %}
                     {{ label }},
                   {% endfor %}
                   ],
        datasets: [{
            label: '# of Votes',
            data: [{% for value in values %}
                     {{ value }},
                   {% endfor %}
                   ],
            fill: false,
            borderColor: [
                'rgb(75, 192, 192)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
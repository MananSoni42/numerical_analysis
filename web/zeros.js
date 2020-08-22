var ctx = document.getElementById('myChart').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: [0, 1, 2, 3, 4, 5, 6],
        datasets: [{
            label: 'y = f(x)',
            data: [0, 10, 5, -2, 20, 30, 45],
            borderColor: "#3e95cd",
            fill: false
        },{
            label: 'solution',
            data: [34,-20, 10, 20, 30, -10, -50],
            borderColor: "#ff0015",
            fill: false
        }]
    },
    options: {}
});

var ctx2 = document.getElementById('myChart2').getContext('2d');
var chart = new Chart(ctx2, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: [0, 1, 2, 3, 4, 5, 6],
        datasets: [{
            label: 'y = f(x)',
            data: [0, 10, 5, -2, 20, 30, 45],
            borderColor: "#3e95cd",
            fill: false
        }]
    },
    options: {}
});

// Slider function
$(document).ready(function() {
  const $valueSpan = $('.valueSpan2');
  const $value = $('#customRange11');
  $valueSpan.html($value.val());
  $value.on('input change', () => {
    $valueSpan.html($value.val());
  });
});

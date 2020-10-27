const range = (start, stop, step = 1) =>
  Array(Math.ceil((stop - start) / step)).fill(start).map((x, y) => x + y * step)

function chart2_label(val) {
    chart2.data.datasets[0].label = `f^(${val})(x0)`;
    chart2.data.datasets[0].label = `f^(${val})(x)`;
    chart2.update();
}

// Canvas js supports zoom
var ctx = document.getElementById('chart-main').getContext('2d');
var chart1 = new Chart(ctx, {
    type: 'line',
    data: {
        datasets: [{
            label: 'f(x)',
            data: [
                {'x': 0, 'y': 9 },
                {'x': 1, 'y': 5 },
                {'x': 2, 'y': 0 },
                {'x': 3, 'y': -7 },
                {'x': 4, 'y': 2 },
                {'x': 5, 'y': -3 }

              ],
            borderColor: "#3e95cd",
            fill: false,
            radius: 0,
        }]
    },
    options: {
        responsive: true,
        scales: {
            xAxes: [{
                type: 'linear',
                position: 'bottom',
                scaleLabel: {
                    display: true,
                    labelString: 'X-axis'
                },
            }],
            yAxes: [{
                type: 'linear',
                position: 'left',
                scaleLabel: {
                    display: true,
                    labelString: 'Y-axis'
                },
            }],
        },
    }
});

var ctx2 = document.getElementById('chart-iter').getContext('2d');
var chart2 = new Chart(ctx2, {
    type: 'line',
    data: {
        datasets: [{
            label: `f^(1)(x0)`,
            data: [
                  {'x': 2, 'y': 1.778 }
              ],
            borderColor: "#000000",
            fill: false,
            radius: 5,
        }, {
            label: `f^(1)(x)`,
            data: [
                  {'x': 0, 'y': 10,               },
                  {'x': 1, 'y': 4.239999999994762 },
                  {'x': 2, 'y': 1.7787537091925576 },
                  {'x': 3, 'y': 1.0708684561906807 },
                  {'x': 4, 'y': 1.000703237621941 },
                  {'x': 5, 'y': 1.0000000706348295 }
              ],
            borderColor: "#d11313",
            fill: false,
            radius: 0,
        }],
    },
    options: {
        responsive: true,
        scales: {
            xAxes: [{
                type: 'linear',
                position: 'bottom',
                scaleLabel: {
                    display: true,
                    labelString: 'Number of iterations'
                },
            }],
            yAxes: [{
                type: 'linear',
                position: 'left',
                scaleLabel: {
                    display: true,
                    labelString: 'X-value'
                },
                ticks: {
                    suggestedMin: 0,
                    suggestedMax: 10,
                }
            }],
        },
    }
});

// Send a request to the server
$("#params").submit(function(e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.
    var form = $(this);
    var url = form.attr('action');
    $.ajax({
           type: "POST",
           url: '/api/diff',
           data: form.serialize(), // serializes the form's elements.
           success: function(response) {
               if (response['error']) {
                   alert(response['err_message'])
               }
               else {
                   chart1.data.datasets[0].data = response['f'];
                   chart1.update();
                   chart2.data.datasets[0].data = response['x0'];
                   chart2.data.datasets[1].data = response['f_'];
                   chart2.options.scales.yAxes[0].ticks.suggestedMax = response['y_max'];
                   chart2.options.scales.yAxes[0].ticks.suggestedMin = response['y_min'];
                   chart2.update();
               }
           },
    });
});

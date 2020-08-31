const range = (start, stop, step = 1) =>
  Array(Math.ceil((stop - start) / step)).fill(start).map((x, y) => x + y * step)

// Canvas js supports zoom
var ctx = document.getElementById('chart-main').getContext('2d');
var chart1 = new Chart(ctx, {
    type: 'line',
    data: {
        datasets: [{
            label: 'solution',
            data: [
                  {'n': 0, 'x': 10,                 'y': 144},
                  {'n': 1, 'x': 4.239999999994762,  'y': 33.17759999992939},
                  {'n': 2, 'x': 1.7787537091925576, 'y': 6.057733303929069},
                  {'n': 3, 'x': 1.0708684561906807, 'y': 0.5011015314176155},
                  {'n': 4, 'x': 1.000703237621941,  'y': 0.00492315789673929},
                  {'n': 5, 'x': 1.0000000706348295, 'y': 4.944438117759277e-07}
              ],
            borderColor: "#d11313",
            fill: false,
            radius: 5,
            },  {
            label: 'y = f(x)',
            data: [
                {'x': -1,'y': -10}, {'x': -0.5, 'y': -8.25},
                {'x': 0, 'y': -6},  {'x': 0.5,  'y': -3.25},
                {'x': 1, 'y': 0},   {'x': 1.5,  'y': 3.75},
                {'x': 2, 'y': 8},   {'x': 2.5,  'y': 12.75},
                {'x': 3, 'y': 18},  {'x': 3.5,  'y': 23.75},
                {'x': 4, 'y': 30},  {'x': 4.5,  'y': 36.75},
                {'x': 5, 'y': 44},  {'x': 5.5,  'y': 51.75},
                {'x': 6, 'y': 60},  {'x': 6.5,  'y': 68.75},
                {'x': 7, 'y': 78},  {'x': 7.5,  'y': 87.75},
                {'x': 8, 'y': 98},  {'x': 8.5,  'y': 108.75},
                {'x': 9, 'y': 120}, {'x': 9.5,  'y': 131.75},
                {'x': 10,'y': 144}
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
        tooltips: {
            callbacks: {
                title: function(item, data) {
                    return "";
                },
                label: function(item, data) {
                    var ind = item.datasetIndex;
                    var x = +data.datasets[ind].data[item.index].x.toFixed(3);
                    var y = +data.datasets[ind].data[item.index].y.toFixed(3);
                    if (ind == 0) {
                        var n = data.datasets[ind].data[item.index].n
                        return "n: " + n + " x: " + x + " y: " + y;
                    }
                    else {
                        return "x: " + x + " y: " + y;
                    }
                }
            }
        }
    }
});

var ctx2 = document.getElementById('chart-iter').getContext('2d');
var chart2 = new Chart(ctx2, {
    type: 'line',
    data: {
        datasets: [{
            label: 'Solution',
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
            tension: 0,
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
            }],
        },
        tooltips: {
            callbacks: {
                title: function(item, data) {
                    return "";
                },
                label: function(item, data) {
                    var ind = item.datasetIndex;
                    // Note the plus sign that drops any "extra" zeroes at the end.
                    // It changes the result (which is a string) into a number again (think "0 + foo"),
                    // which means that it uses only as many digits as necessary.
                    var x = +data.datasets[ind].data[item.index].x.toFixed(3);
                    var y = +data.datasets[ind].data[item.index].y.toFixed(3);
                    if (ind == 0) {
                        var n = data.datasets[ind].data[item.index].n
                        return "n: " + n + " x: " + x + " y: " + y;
                    }
                    else {
                        return "x: " + x + " y: " + y;
                    }
                }
            }
        }
    }
});

// Send a request to the server
$("#params").submit(function(e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.
    var form = $(this);
    var url = form.attr('action');
    $.ajax({
           type: "POST",
           url: '/api/zeroes',
           data: form.serialize(), // serializes the form's elements.
           success: function(response) {
               if (response['error']) {
                   alert(response['err_message'])
               }
               else {
                   chart1.data.datasets[0].data = response['sols']
                   chart1.data.datasets[1].data = response['f']
                   chart1.update()
                   chart2.data.datasets[0].data = response['num_f']
                   chart2.update()
                   $('#sol_ans').html(response['sol'])
                   $('#sol_itr').html(response['num_iter'])
                   $('#sol_tol').html(response['tol'])
                   $('#sol_conv').html(response['ord_conv'])
               }
           },
    });
});

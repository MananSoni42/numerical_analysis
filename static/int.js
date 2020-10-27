var ctx = document.getElementById('chart-main').getContext('2d');
var chart1 = new Chart(ctx, {
    type: 'line',
    data: {
        datasets: [{
            label: 'y = f(x)',
            data: [
                {'x': 10, 'y': 14},
                {'x': 1, 'y': 4},
                {'x': -2, 'y': 5},
              ],
            borderColor: "#3e95cd",
            fill: true,
            radius: 0,
        }, {
            type: 'scatter',
            label: 'integration pts',
            data: [
                {'x': -1, 'y': 0},
                {'x': 0, 'y': 0},
                {'x': 1, 'y': 0},
              ],
            borderColor: "#000000",
            fill: false,
            radius: 1,
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
    },
});

function get_int_eq(ans) {
    from = $('#from').val();
    to = $('#to').val();
    f = $('#f').val()

    return `$$ \\int_{${from}}^{${to}} ${f} \\,dx \\approx ${ans.toString()} $$`;
}

// Send a request to the server
$("#params").submit(function(e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.
    var form = $(this);
    var url = form.attr('action');
    $.ajax({
           type: "POST",
           url: '/api/int',
           data: form.serialize(), // serializes the form's elements.
           success: function(response) {
               if (response['error']) {
                   alert(response['err_message'])
               }
               else {
                   chart1.data.datasets[0].data = response['f']
                   chart1.data.datasets[1].data = response['pts']
                   chart1.update()
                   $('#ans').html(get_int_eq(response['ans']))
                   MathJax.Hub.Queue(["Typeset", MathJax.Hub, 'ans']);
               }
           },
    });
});

var ctx = document.getElementById('chart-main').getContext('2d');
var chart1 = new Chart(ctx, {
    type: 'line',
    data: {
        datasets: [{
            label: 'y = f(x)',
            data: [
                {'x': 12, 'y': 0},
                {'x': 10, 'y': 14},
                {'x': 1, 'y': 4},
                {'x': -2, 'y': 5},
                {'x': -4, 'y': 0},
              ],
            borderColor: "#3e95cd",
            fill: false,
            radius: 0,
            order: 2,
        }, {
            type: 'scatter',
            label: 'function points',
            data: [
                {'x': 12, 'y': 0},
                {'x': 10, 'y': 14},
                {'x': 1, 'y': 4},
                {'x': -2, 'y': 5},
                {'x': -4, 'y': 0},
              ],
            borderColor: "#d11313",
            fill: false,
            radius: 3,
            order: 1,
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

$('#super-tol').hide();
function set_tol_h(obj) {
    if (['adam-milne-pc'].includes(obj.value)) {
        $('#super-tol').show();
        $('#super-h').show();
    } else if (['adaptive-euler'].includes(obj.value)) {
        $('#super-tol').show();
        $('#super-h').hide();
    } else {
        $('#super-tol').hide();
        $('#super-h').show();
    }
}

// Send a request to the server
$("#params").submit(function(e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.
    var form = $(this);
    var url = form.attr('action');
    $.ajax({
           type: "POST",
           url: '/api/de',
           data: form.serialize(), // serializes the form's elements.
           success: function(response) {
               if (response['error']) {
                   alert(response['err_message'])
               }
               else {
                   chart1.data.datasets[0].data = response['f']
                   chart1.data.datasets[1].data = response['f']
                   chart1.update()
                   $("#qeq").html("$$ y' = " + response['y_'] + "$$")
                   MathJax.Hub.Queue(["Typeset", MathJax.Hub, 'qjax']);
                   $("#qy0").html(response['init']['y'])
                   $("#qx0").html(response['init']['x'])
               }
           },
    });
});

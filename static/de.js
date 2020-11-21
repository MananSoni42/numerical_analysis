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
        }, {
            type: 'line',
            label: 'exact solution',
            data: [
                {'x': 13, 'y': 0},
                {'x': 9, 'y': 14},
                {'x': 1, 'y': 4},
                {'x': -1, 'y': 5},
                {'x': -3, 'y': 0},
              ],
            borderColor: "#d0e300",
            hidden: hidden,
            fill: false,
            radius: 0,
            order: 3,
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

function set_form(inp) {
    var arr = inp.split(",")
    $("#f").val(arr[1]);
    $("#x0").val(arr[2]);
    $("#y0").val(arr[3]);
    $("#from").val(arr[4]);
    $("#to").val(arr[5]);
    $("#h").val(arr[6]);
}

function set_f_y0(obj) {
    set_form(obj.value);
}

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

$( document ).ready(function() {
    $('#super-tol').hide();
    set_form("1, y, 0, 1, 0, 4, 0.1");
});

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
                   if (!hidden) {
                       chart1.data.datasets[2].data = response['exact']
                   }
                   chart1.update()

                   $("#qeq").html("$$ y' = " + response['y_'] + "$$")
                   MathJax.Hub.Queue(["Typeset", MathJax.Hub, 'qjax']);

                   if (response['type'] == 'ivp') {
                       $("#qy0").html(response['init']['y'])
                       $("#qx0").html(response['init']['x'])
                   } else {
                       $("#qx0").html(response['init']['x0'])
                       $("#qxn").html(response['init']['xn'])
                       $("#qb0").html(response['init']['b'][0])
                       $("#qb1").html(response['init']['b'][1])
                       $("#qb2").html(response['init']['b'][2])
                   }
               }
           },
    });
});

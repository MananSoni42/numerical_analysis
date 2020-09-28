var n = 0

$(document).ready(function() {
    n = 1;
    $('input[name="n"]').val(n);
    $('#matrix-input').html(make_form(n));
});

function make_form(n) {
    var form = ""

    form += `
    <div class="form-group row">
        <label class="col-6 col-form-label text-center">x</label>
        <label class="col-6 col-form-label text-center">f(x)</label>
    </div>
    `;

    for (i=0;i<n;i++) {
        form += `
        <div class="form-group row">
            <div class="col-6">
                <input type="text" class="form-control" id="${i}-0" name="${i}-0">
            </div>
            <div class="col-6">
                <input type="text" class="form-control" id="${i}-1" name="${i}-1">
            </div>
        </div>
        `;
    }

    //console.log(form)
    return form;
}

$("#addeq").click(function(e) {
    e.preventDefault();
    n = n+1;
    $('input[name="n"]').val(n);
    $('#matrix-input').html(make_form(n));
});

$("#subeq").click(function(e) {
    e.preventDefault();
    n = Math.max(1,n-1);
    $('input[name="n"]').val(n);
    $('#matrix-input').html(make_form(n));
});

// Canvas js supports zoom
var ctx = document.getElementById('chart-main').getContext('2d');
var chart1 = new Chart(ctx, {
    type: 'line',
    data: {
        datasets: [{
            label: 'Data points',
            type: 'scatter',
            data: [
                    {'x': 1, 'y': 2},
                    {'x': 2, 'y': 3},
                    {'x': 3, 'y': 4},
              ],
             borderColor: "#d11313",
             fill: false,
             radius: 3,
            },  {
            label: 'P(x)',
            data: [
                {'x': -1,'y': 0},
                {'x': 0, 'y': 1},
                {'x': 1, 'y': 2},
                {'x': 2, 'y': 3},
                {'x': 3, 'y': 4},
                {'x': 4, 'y': 5},
                {'x': 5, 'y': 6},
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

function make_lagrange(coeffs) {
    poly = `${coeffs[0]} P_{${1}}`;
    for (i=1;i<coeffs.length;i++) {
        if (coeffs[i] >= 0) { poly += `+ ${coeffs[i]} P_{${i+1}}`; }
        else { poly += `- ${-coeffs[i]} P_{${i+1}}`; }
    }

    return "$$" + poly + "$$";
}

function make_poly(coeffs) {
    n = coeffs.length
    poly = `${coeffs[0]}x^{${n-1}}`;
    for (i=1;i<coeffs.length-1;i++) {
        if (coeffs[i] >= 0) { poly += `+ ${coeffs[i]} x^{${n-1-i}}`; }
        else { poly += `- ${-coeffs[i]} x^{${n-1-i}}`; }
    }

    if (n > 1) {
        if (coeffs[i] >= 0) { poly += `+ ${coeffs[i]}`; }
        else { poly += `- ${-coeffs[i]}`; }
    }

    return "$$" + poly + "$$";
}

// Send a request to the server
$("#params").submit(function(e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.
    var form = $(this);
    var url = form.attr('action');
    $.ajax({
           type: "POST",
           url: '/api/interp',
           data: form.serialize(), // serializes the form's elements.
           success: function(response) {
               if (response['error']) {
                   alert(response['err_message'])
               }
               else {
                   chart1.data.datasets[0].data = response['data']
                   chart1.data.datasets[1].data = response['poly']
                   chart1.update()
                   $('#sol_unsimple').html(make_lagrange(response['unsimple']))
                   $('#sol_simple').html(make_poly(response['simple']))
                   MathJax.Hub.Queue(["Typeset", MathJax.Hub, 'sol_unsimple']);
                   MathJax.Hub.Queue(["Typeset", MathJax.Hub, 'sol_simple']);
               }
           },
    });
});

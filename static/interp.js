var n = 0
var cols = 2;

$(document).ready(function() {
    n = 1;
    $('input[name="n"]').val(n);
    $('#matrix-input').html(make_form(n));
});

function make_form(n) {
    var form = ""

    form += `
    <div class="form-group row mb-0 mt-3">
        <label class="col-4 col-form-label text-center">x</label>
        <label class="col-4 col-form-label text-center">f(x)</label>
        <label class="col-4 col-form-label text-center">f'(x) <small> optional <small></label>
    </div>
    `;

    for (i=0;i<n;i++) {
        form += `
        <div class="form-group row">
            <div class="col-4">
                <input type="text" class="form-control" id="${i}-0" name="${i}-0">
            </div>
            <div class="col-4">
                <input type="text" class="form-control" id="${i}-1" name="${i}-1">
            </div>
            <div class="col-4">
                <input type="text" class="form-control" id="${i}-2" name="${i}-2" placeholder="-">
            </div>
        </div>
        `;
    }

    return form;
}

function getform(n) {
    var x = [], y = [], z = [];
    for (var i=0;i<n;i++) {
        x.push($(`#${i}-0`).val())
        y.push($(`#${i}-1`).val())
        z.push($(`#${i}-2`).val())
    }
    return [x,y,z];
}

function fillform(n, data) {
    m = data[0].length;
    for (var i=0;i<Math.min(m,n);i++) {
        $(`#${i}-0`).val(data[0][i])
        $(`#${i}-1`).val(data[1][i])
        $(`#${i}-2`).val(data[2][i])
    }
}

$("#addeq").click(function(e) {
    e.preventDefault();

    var pts = getform(n);
    n = n+1;
    $('input[name="n"]').val(n);
    $('#matrix-input').html(make_form(n));
    fillform(n, pts);
});

$("#subeq").click(function(e) {
    e.preventDefault();

    var pts = getform(n);
    n = Math.max(1,n-1);
    $('input[name="n"]').val(n);
    $('#matrix-input').html(make_form(n));
    fillform(n, pts)
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

function make_special(coeffs, v) {
    start = 1;
    if (v == 'N') { start = 0; }
    poly = `${coeffs[0]} ${v}_{${start}}`;
    for (i=start;i<coeffs.length;i++) {
        if (coeffs[i] >= 0) { poly += `+ ${coeffs[i]} ${v}_{${i+1}}`; }
        else { poly += `- ${-coeffs[i]} ${v}_{${i+1}}`; }
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
                   console.log(response['lagrange']);
                   console.log(response['newton']);                   
                   $('#sol_lagrange').html(make_special(response['lagrange'], 'L'))
                   $('#sol_newton').html(make_special(response['newton'], 'N'))
                   $('#sol_simple').html(make_poly(response['simple']))
                   MathJax.Hub.Queue(["Typeset", MathJax.Hub, 'sol_unsimple']);
                   MathJax.Hub.Queue(["Typeset", MathJax.Hub, 'sol_simple']);
               }
           },
    });
});

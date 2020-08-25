const range = (start, stop, step = 1) =>
  Array(Math.ceil((stop - start) / step)).fill(start).map((x, y) => x + y * step)

var ctx = document.getElementById('myChart').getContext('2d');

var chart = new Chart(ctx, {
    type: 'line',
    data: {
        datasets: [{
            label: 'solution',
            data: [
                  {'x': 10, 'y': 144},
                  {'x': 4.239999999994762, 'y': 33.17759999992939},
                  {'x': 1.7787537091925576, 'y': 6.057733303929069},
                  {'x': 1.0708684561906807, 'y': 0.5011015314176155},
                  {'x': 1.000703237621941, 'y': 0.00492315789673929},
                  {'x': 1.0000000706348295, 'y': 4.944438117759277e-07}
              ],
            borderColor: "#d11313",
            fill: false,
            radius: 5,
            },  {
            label: 'y = f(x)',
            data: [
                {x: -1, y: -10}, {x: -0.5, y: -8.25},
                {x: 0, y: -6}, {x: 0.5, y: -3.25},
                {x: 1, y: 0}, {x: 1.5, y: 3.75},
                {x: 2, y: 8}, {x: 2.5, y: 12.75},
                {x: 3, y: 18}, {x: 3.5, y: 23.75},
                {x: 4, y: 30}, {x: 4.5, y: 36.75},
                {x: 5, y: 44}, {x: 5.5, y: 51.75},
                {x: 6, y: 60}, {x: 6.5, y: 68.75},
                {x: 7, y: 78}, {x: 7.5, y: 87.75},
                {x: 8, y: 98}, {x: 8.5, y: 108.75},
                {x: 9, y: 120}, {x: 9.5, y: 131.75},
                {x: 10, y: 144}
                 ],
            borderColor: "#3e95cd",
            fill: false
        }]
    },
    options: {
        scales: {
            xAxes: [{
                type: 'linear',
                position: 'bottom'
            }]
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
           url: 'na-bits.herokuapp.com',
           data: form.serialize(), // serializes the form's elements.
           success: function(response) {
               if (response['error']) {
                   alert(response['err_message'])
               }
               else {
                   chart.data.datasets[0].data = response['sols']
                   chart.data.datasets[1].data = response['f']
                   chart.update()
                   $('#sol_ans').html(response['sol'])
                   $('#sol_itr').html(response['num_iter'])
                   $('#sol_tol').html(response['tol'])
                   $('#sol_conv').html(response['ord_conv'])
               }
           },
    });
});

var n = 2

function make_form(n) {
    var margin = 12 - 2*(n+1)
    var form = ""

    margin_line = ""
    if (margin != 0) { margin_line = `<label class="col-${margin} col-form-label text-center"></label>` }
    form += `
        <div class="form-group row">
            <label class="col-${2*n} col-form-label text-center">A</label>
            ${margin_line}
            <label class="col-2 col-form-label text-center">B</label>
        </div>
    `;

    for (i=0;i<n;i++) {
        form += '<div class="form-group row">'
        for (j=0;j<n;j++) {
            border = "";
            if (j == n-1) { border = "border-right"; }
            form += `
            <div class="col-md-2 ${border}">
                <input type="text" class="form-control" id="${i}-${j}" name="${i}-${j}">
            </div>
            `;
        }
        if (margin != 0) {
            form += `<div class="col-md-${margin}"></div>`;
        }
        form += `
        <div class="col-md-2">
            <input type="text" class="form-control" id="${i}-${n}" name="${i}-${n}">
        </div>
        `;

        form += '</div>'
    }
    //console.log(form)
    return form;
}

$("#addeq").click(function(e) {
    e.preventDefault();
    n = Math.min(5,n+1);
    console.log(n)
    $('#matrix-input').html(make_form(n));
});

$("#subeq").click(function(e) {
    e.preventDefault();
    n = Math.max(1,n-1);
    console.log(n)
    $('#matrix-input').html(make_form(n));
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

var n = 0

$(document).ready(function() {
    n = 2;
    $('input[name="n"]').val(n);
    $('#matrix-input').html(make_form(n));
});

function make_form(n) {
    var margin = 12 - 2*(n+1)
    var form = ""

    margin_line = ""
    if (margin != 0) { margin_line = `<label class="col-${margin} col-form-label text-center"></label>` }
    form += `
        <div class="form-group row mb-0">
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
            <div class="col-2 ${border}">
                <input type="text" class="form-control" id="${i}-${j}" name="${i}-${j}">
            </div>
            `;
        }
        if (margin != 0) {
            form += `<div class="col-${margin}"></div>`;
        }
        form += `
        <div class="col-2">
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
    $('input[name="n"]').val(n);
    $('#matrix-input').html(make_form(n));
});

$("#subeq").click(function(e) {
    e.preventDefault();

    n = Math.max(1,n-1);
    $('input[name="n"]').val(n);
    $('#matrix-input').html(make_form(n));
});

function addTable(id, dataArray) {
  var myTable = document.createElement('table');
  myTable.setAttribute('class', 'table table-responsive table-borderless text-warning')

  $('#'+id).empty()
  document.getElementById(id).appendChild(myTable);

  var y = document.createElement('tr');
  myTable.appendChild(y);

  for(var i = 0 ; i < dataArray.length ; i++) {
    var row= dataArray[i];
    var y2 = document.createElement('tr');
    for(var j = 0 ; j < row.length ; j++) {
      myTable.appendChild(y2);
      var th2 = document.createElement('td');
      var date2 = document.createTextNode(+row[j].toFixed(7));
      th2.appendChild(date2);
      y2.appendChild(th2);
    }
  }
}

// Send a request to the server
$("#params").submit(function(e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.
    var form = $(this);
    var url = form.attr('action');
    $.ajax({
           type: "POST",
           url: '/api/lineq',
           data: form.serialize(), // serializes the form's elements.
           success: function(response) {
               console.log(response)
               if (response['error']) {
                   alert(response['err_message'])
               }
               else {
                   $('#sol_cond').html(+response['cond'].toFixed(3))

                   if (response['diag'] == 1) { $('#sol_diag1').html('True') }
                   else { $('#sol_diag1').html('False') }

                   if (response['diag_transform'] == 1) { $('#sol_diag2').html('True') }
                   else { $('#sol_diag2').html('False') }

                   addTable('sol_diag3', response['A_diag'])
                   addTable('sol_ans', response['sol'])

                   $('#sol_itr').html(response['num_iter'])
               }
           },
    });
});

$('.radioBtn a').on('click', function(){
    var sel = $(this).data('title');
    var tog = $(this).data('toggle');
    $('#'+tog).prop('value', sel);

    $('a[data-toggle="'+tog+'"]').not('[data-title="'+sel+'"]').removeClass('active').addClass('notActive');
    $('a[data-toggle="'+tog+'"][data-title="'+sel+'"]').removeClass('notActive').addClass('active');
})

$('#thyroid_form').submit(function (event) {
    event.preventDefault();
    var form = document.getElementById('thyroid_form');
    var formData = new FormData(form);

    var object = {};
    formData.forEach(function(value, key) {
        if (value === "true") {
            object[key] = true
        }
        else if (value === "false") {
            object[key] = false
        }
        else if (!isNaN(value) && value.trim() != "") {
            object[key] = parseFloat(value)
        }
        else {
            object[key] = value;
        }

    });

    var json = JSON.stringify(object);

    console.log(json);

    $.ajax({
        url: 'http://localhost:8000',
        method: 'POST',
        contentType: "application/json; charset=utf-8",
        data: json,
        processData: false,
        success: function (response) {
            console.log(response)
            enableResultButton(response.prediction)
        },
        error: function (xhr, status, error) {
            alert('Your form was not sent successfully.');
            console.error(error);
        }
    });
});

function disableAllResultButtons() {
    var elements = document.querySelectorAll('.result-buttons');

    for (var i = 0; i < elements.length; i++) {
        elements[i].classList.remove('active');
        elements[i].classList.remove('notActive');
        elements[i].classList.add('notActive');
        elements[i].classList.add('disabled');
    }
}

function enableResultButton(name) {
    disableAllResultButtons()

    var elements = document.querySelectorAll('#' + name);
    for (var i = 0; i < elements.length; i++) {
        elements[i].classList.remove('notActive');
        elements[i].classList.remove('disabled');
        elements[i].classList.add('active');
    }

    var elements = document.querySelectorAll('.result-container');
    for (var i = 0; i < elements.length; i++) {
        if (elements[i].classList.contains('d-none')) {
            elements[i].classList.remove('d-none');
        }
    }
}

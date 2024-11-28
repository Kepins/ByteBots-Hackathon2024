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
        object[key] = value;
    });

    var json = JSON.stringify(object); // Convert the plain object to JSON

    console.log(json);

    $.ajax({
        url: 'http://localhost:8000',
        method: 'POST',
        contentType: "application/json; charset=utf-8",
        data: json,
        processData: false, // No processing of data
        success: function (response) {
            alert('Form submitted successfully: ' + response);
        },
        error: function (xhr, status, error) {
            alert('Your form was not sent successfully.');
            console.error(error);
        }
    });
});

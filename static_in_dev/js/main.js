$(document).on('change', '.input-files-js', (e) => {
    const $this = $(e.target),
        // $label = $this.next('label'),
        $files = $this[0].files;

    if ($files && $files.length > 1)
        $('.custom-file-label').html($files.length + ' файлов выбранно')
});

$(document).ready(function () {

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    $('#link').on('click', function (e) {
        e.preventDefault();
        let data;
        $.ajax({
            type: 'GET',
            url: '/getlink/',
            success: function (data) {
                const url = window.location.origin + '/media/' + data.directory + '/images.zip';
                $(location).attr('href', url);
                data = {
                    status: true,
                    csrfmiddlewaretoken: csrftoken,
                }
                // $.ajaxSetup({
                //     data: {csrfmiddlewaretoken: csrftoken},
                // });
                $.ajax({
                    type: 'POST',
                    url: '/getlink/',
                    data: data,
                    dataType: 'json',
                    success: setTimeout(function (data) {
                        const url = window.location.origin;
                        $(location).attr('href', url);
                    }, 1000),
            })
            },
            error: function (e) {
                alert('Что пошло не так...');
            }
        });
    })
});

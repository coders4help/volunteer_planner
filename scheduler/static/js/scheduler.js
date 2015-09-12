$(document).ready(function () {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?

                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });
    $('.add-button').on('click', function () {
        var participate_wish = $(this).parent().attr('data-need-id');
        $.ajax({
            type: "POST",
            url: "/helpdesk/registerforneed/",
            data: {
                'id_need': participate_wish
            },
            async: false,
            success: function (data) {
            location.reload();
            }
        });
    })
        $('.delete-button').on('click', function () {
            var participate_wish = $(this).parent().attr('data-need-id');
            $.ajax({
                type: "POST",
                url: "/helpdesk/deregisterforneed/",
                data: {
                    'id_need': participate_wish
                },
                async: false,
                success: function (data) {
                location.reload();
                }
            });


        })
    })

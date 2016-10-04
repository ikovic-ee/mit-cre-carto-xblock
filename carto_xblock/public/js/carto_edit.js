function StudioEdit(runtime, element) {
    $(element).find('.save-button').bind('click', function () {
        var handlerUrl = runtime.handlerUrl(element, 'studio_submit');

        var data = new FormData();
        data.append('display_name', $(element).find('input[name=display_name]').val());
        data.append('display_description', $(element).find('input[name=display_description]').val().trim());
        data.append('thumbnail', $(element).find('input[name=thumbnail]').val().trim());

        runtime.notify('save', {state: 'start'});

        $.ajax({
            url: handlerUrl,
            type: 'POST',
            data: data,
            cache: false,
            dataType: 'json',
            processData: false,
            contentType: false
        }).done(function (response) {
            runtime.notify('save', {state: 'end'});
        });
    });

    $(element).find('.cancel-button').bind('click', function () {
        runtime.notify('cancel', {});
    });
}

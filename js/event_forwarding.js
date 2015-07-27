$(document).ready(function() {
    var EVENTS_ENDPOINT = '/events';
    var MAIN_MEDIA_ID = '#main-media';


    var nameOfMouseButton = Object.create(null);
    nameOfMouseButton[1] = 'left';
    nameOfMouseButton[2] = 'middle';
    nameOfMouseButton[3] = 'right';

    var mouseEventHandler = function(event) {
        notifyEvent({
            type: event.type,
            content: {
                button: nameOfMouseButton[event.which],
                coordinates: {
                    x: event.pageX,
                    y: event.pageY
                }
            }
        });
    };

    var notifyEvent = function(eventData) {
        $.post(EVENTS_ENDPOINT, eventData, function(responseData, statusCode) {
            if (statusCode !== '200') return;

            var newMediaUrl = responseData.media.content;
            $(MAIN_MEDIA_ID).attr('src', newMediaUrl);
        }, 'json');
    };


    $(MAIN_MEDIA_ID).mousedown(mouseEventHandler);
    $(MAIN_MEDIA_ID).mouseup(mouseEventHandler);
});

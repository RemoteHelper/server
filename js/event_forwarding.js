$(document).ready(function() {
    "use strict";

    var EVENTS_ENDPOINT = '/events';
    var MAIN_MEDIA_ID = '#main-media';

    var nameOfMouseButton = Object.create(null);
    nameOfMouseButton[1] = 'left';
    nameOfMouseButton[2] = 'middle';
    nameOfMouseButton[3] = 'right';



    /* Mouse event handling */
    var mouseHandler = function(event) {
        notifyEvent(pickMouseEventData(event));
    };

    var notifyEvent = function(eventData) {
        $.ajax({
            type: 'POST',
            url: EVENTS_ENDPOINT,
            data: JSON.stringify(eventData),
            contentType: 'application/json',
            success: function(responseData, statusCode) {
                console.log(responseData.statusCode);
                if (statusCode !== '200') return;

                var newMediaUrl = responseData.media.content;
                $(MAIN_MEDIA_ID).attr('src', newMediaUrl);
            },
            error: function() {
                console.log(arguments);
            }
        });
    };

    var pickMouseEventData = function(event) {
        var mouseEventData = pickCommonEventData(event);
        mouseEventData.content = {
            button: nameOfMouseButton[event.which],
            coordinates: {
                x: event.pageX,
                y: event.pageY
            }
        };

        return mouseEventData;
    };

    var pickCommonEventData = function(event) {
        return {
            type: event.type,
            timestamp: event.timeStamp
        };
    };



    /* Keyboard events handler */
    var keydownHandler = function(event) {
        if (isJustAModifierKey(event)) return;

        notifyEvent(pickKeydownData(event));
    };

    var pickKeydownData = function(event) {
        var keydownData = pickCommonEventData(event);
        keydownData.content = {
            code: event.which,
            modifiers: ['ctrlKey', 'altKey', 'shiftKey', 'metaKey'].filter(function(modifierKeyName) {
                return event[modifierKeyName];
            })
        };

        return keydownData;
    };

    var isJustAModifierKey = function(event) {
        // see http://unixpapa.com/js/key.html
        return [
            16, // Shift
            17, // Ctrl || Left and Right Command (Opera)
            18, // Alt
            91, // Left Command (Safari)
            224, // Left and Right Command (Firefox)
            93 // Right Command (Safari)
        ].indexOf(event.which) !== -1;
    };



    /* Hook handlers */
    $(MAIN_MEDIA_ID).mousedown(mouseHandler);
    $(MAIN_MEDIA_ID).mouseup(mouseHandler);

    $(this).keydown(keydownHandler);
});
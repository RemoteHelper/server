$(document).ready(function() {
    "use strict";

    var EVENTS_ENDPOINT = '/events';
    var MAIN_MEDIA_ID = '#main-media';

    var nameOfMouseButton = Object.create(null);
    nameOfMouseButton[1] = 'left';
    nameOfMouseButton[2] = 'middle';
    nameOfMouseButton[3] = 'right';

    // Add click animation every time the user clicks on the media
    $('#media-container').on('mousedown', function (e) {
        $('i')
            .addClass('active')
            .css('left', e.pageX)
            .css('top', e.pageY);
    });

    // As soon as the animation ends, remove it
    $('i').bind('transitionend webkitTransitionEnd oTransitionEnd MSTransitionEnd',  function () {
       $('i').removeClass('active');
    });



    /* Mouse event handling */
    var mouseHandler = function(event) {
        notifyEvent(pickMouseEventData(event));
    };

    var notifyEvent = function(eventData) {
        if (RemoteHelper.isHelpJobDone()) return;

        $.ajax({
            type: 'POST',
            url: EVENTS_ENDPOINT,
            data: JSON.stringify(eventData),
            contentType: 'application/json',
            dataType: "json",
            success: function(responseData) {
                var newMediaURL = responseData['mediaURL'] + '?' + Math.random();
                $(MAIN_MEDIA_ID).attr('src', newMediaURL);
            },
            error: function() {
                console.log(arguments);
            }
        });
    };

    var pickMouseEventData = function(event) {
        var mouseEventData = pickCommonEventData(event);
        var relativeCoordinates = getRelativeCoordinates(event);
        mouseEventData.content = {
            button: nameOfMouseButton[event.which],
            coordinates: {
                x: relativeCoordinates.x,
                y: relativeCoordinates.y
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

    var getRelativeCoordinates = function(event) {
        var target = event.target;
        var root_element = document.getElementsByTagName('html')[0];

        var relX = event.clientX - target.offsetLeft + root_element.scrollLeft,
            relY = event.clientY - target.offsetTop + root_element.scrollTop;

        var totalW = target.videoWidth || target.naturalWidth,
            totalH = target.videoHeight || target.naturalHeight;

        var scaleX = totalW / target.clientWidth,
            scaleY = totalH / target.clientHeight;

        return {
            "x": Math.round(relX * scaleX),
            "y": Math.round(relY * scaleY)
        };
    };



    /* Keyboard events handler */
    var keydownHandler = function(event) {
        if (isJustAModifierKey(event.which)) return;

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

    var isJustAModifierKey = function(keyIdentifier) {
        // see http://unixpapa.com/js/key.html
        return [
            16, // Shift
            17, // Ctrl || Left and Right Command (Opera)
            18, // Alt
            91, // Left Command (Safari)
            224, // Left and Right Command (Firefox)
            93 // Right Command (Safari)
        ].indexOf(keyIdentifier) !== -1;
    };



    /* Hook handlers */
    $(MAIN_MEDIA_ID).mousedown(mouseHandler);
    $(MAIN_MEDIA_ID).mouseup(mouseHandler);

    $(this).keydown(keydownHandler);
});

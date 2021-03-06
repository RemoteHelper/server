window.RemoteHelper = (function() {
    "use strict";

    var sourcePath = '/api/done';
    var INSTRUCTIONS_ID = '#instructions';
    var helpJobDoneStatus = false;

    var checkDoneStatus = function() {
        $.ajax({
            type: 'GET',
            url: sourcePath,
            dataType: 'json',
            success: function(response) {
                if (!response.done) return;

                helpJobDoneStatus = response.done;

                if (response.hasOwnProperty('doneText')) {
                    $(INSTRUCTIONS_ID)
                        .text(response.doneText);
                }

                stopPolling();
            }
        });
    };

    var stopPolling = function() {
        clearInterval(intervalId);
    };

    var intervalId = setInterval(checkDoneStatus, 500);

    return {
        isHelpJobDone: function() {
            return helpJobDoneStatus;
        }
    };
}());

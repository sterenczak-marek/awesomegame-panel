function sendAjax(parameters) {
    var url = parameters.url;
    var method = parameters.method;
    var success = parameters.success;
    var complete = parameters.complete;

    $.ajax({
        url: url,
        method: method,
        success: success,
        complete: complete
    });
}

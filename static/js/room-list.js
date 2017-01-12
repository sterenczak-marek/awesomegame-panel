var datatable_dom = $('#datatable-responsive');

var roomTable = datatable_dom.DataTable({
    ajax: {
        url: datatable_dom.data('url'),
        dataSrc: "results"
    },
    serverSide: true,
    ordering: false,
    columns: [
        {
            "data": "name",
            "render": function (data, type, full, meta) {
                return '<a href="' + full.url + '">' + data + '</a>'
            }
        },
        {
            "data": "users",
            "render": function (data, type, full, meta) {
                players = "";
                if (data.length) {
                    $.each(data, function (index, item) {
                        players += item.username;
                        if (index + 1 != data.length)
                            players += ", "
                    });
                    return players;
                } else {
                    return 'PUSTY';
                }
            }
        },
    ]
});


function receiveMessage(msg) {
    setTimeout(function () {
        roomTable.ajax.reload(null, false);
    }, 1000);
}

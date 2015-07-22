/**
 * Created by johannes on 7/20/15.
 */

function load_view(url) {
    $.ajax({
        url: url,
        dataType: 'json',
        cache: false,
        success: function (data) {
            $("#devviz-views").append(data.content);
        }.bind(this),
        error: function (xhr, status, err) {
            console.error(this.props.url, status, err.toString());
        }.bind(this)
    });
}

function reload_view(url, type, viewid) {
    $.ajax({
        url: url,
        type: type,
        dataType: 'json',
        cache: false,
        success: function (data) {
            $("#view-" + viewid).replaceWith(data.content);
        }.bind(this),
        error: function (xhr, status, err) {
            console.error(this.props.url, status, err.toString());
        }.bind(this)
    });
}

function add_var(viewid, variable) {
    var url = "/views/" + viewid + "/" + variable;
    reload_view(url, 'POST', viewid);
}

function del_var(viewid, variable) {
    var url = "/views/" + viewid + "/" + variable;
    reload_view(url, 'DELETE', viewid);
}

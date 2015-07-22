/**
 * Created by johannes on 7/17/15.
 */

var VariableTable = React.createClass({displayName: "VariableTable",
    getInitialState: function() {
        return {data: []};
    },
    componentWillMount: function(){
        var stream = new EventSource("/variables/stream");
        stream.addEventListener("message", this.process, false);
    },
    process: function(e) {
        var payload = JSON.parse(e.data);
        this.setState({data: payload.data});
    },
    componentDidMount: function() {
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            cache: false,
            success: function(data) {
                this.setState({data: data.data});
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    render: function() {
        var variableNodes = this.state.data.map(function (variable) {
            return (
                React.createElement(Variable, {name: variable.name, type: variable.type})
            );
        });
        return (
            React.createElement("table", {className: "table table-striped"}, 
                React.createElement("thead", null, 
                React.createElement("tr", null, React.createElement("th", null, "Name"), React.createElement("th", null, "Type"))
                ), 
                React.createElement("tbody", null, 
                variableNodes
                )
            )
        );
    }
});
var Variable = React.createClass({displayName: "Variable",
    render: function() {
        return (
            React.createElement("tr", null, React.createElement("td", null, this.props.name), React.createElement("td", null, this.props.type))
        );
    }
});


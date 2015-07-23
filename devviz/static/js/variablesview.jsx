/**
 * Created by johannes on 7/17/15.
 */

var VariableTable = React.createClass({
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
                <Variable name={variable.name} type={variable.type} />
            );
        });
        return (
            <div className="container" id="variables">
                {variableNodes}
            </div>
        );
    }
});
var Variable = React.createClass({
    render: function() {
        var classString = 'variable ' + this.props.type;
        return (
            <div className={classString} id={this.props.name}>{this.props.name}</div>
        );
    }
});


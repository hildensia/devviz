/**
 * Created by johannes on 7/24/15.
 */
// set up our data series with 150 random data points

function create_graph (variables, viewid) {
    var palette = new Rickshaw.Color.Palette( { scheme: 'spectrum2001' } );
    var seriesData = [];
    for (variable of variables) {
        var data = { color: palette.color(),
            data: [{'x': 0, 'y': 0}],
            name: variable};
        seriesData.push(data);
    }

    // instantiate our graph!
    var graph = new Rickshaw.Graph( {
        element: document.getElementById("chart-" + viewid),
        width: 830,
        height: 500,
        renderer: 'area',
        stroke: true,
        preserve: true,
        min: 'auto',
        series: seriesData});

    graph.render();

    var preview = new Rickshaw.Graph.RangeSlider( {
        graph: graph,
        element: document.getElementById('preview-' + viewid)
    } );

    var hoverDetail = new Rickshaw.Graph.HoverDetail( {
        graph: graph,
        xFormatter: function(x) {
            return new Date(x * 1000).toString();
        }
    } );

    var annotator = new Rickshaw.Graph.Annotate( {
        graph: graph,
        element: document.getElementById('timeline-' + viewid)
    } );

    var legend = new Rickshaw.Graph.Legend( {
        graph: graph,
        element: document.getElementById('legend-' + viewid)
    } );

    var shelving = new Rickshaw.Graph.Behavior.Series.Toggle( {
        graph: graph,
        legend: legend
    } );

    var order = new Rickshaw.Graph.Behavior.Series.Order( {
        graph: graph,
        legend: legend
    } );

    var highlighter = new Rickshaw.Graph.Behavior.Series.Highlight( {
        graph: graph,
        legend: legend
    } );

    var smoother = new Rickshaw.Graph.Smoother( {
        graph: graph,
        element: document.querySelector('#smoother-' + viewid)
    } );

    var ticksTreatment = 'glow';

    var xAxis = new Rickshaw.Graph.Axis.Time( {
        graph: graph,
        ticksTreatment: ticksTreatment,
        timeFixture: new Rickshaw.Fixtures.Time.Local()
    } );

    xAxis.render();

    var yAxis = new Rickshaw.Graph.Axis.Y( {
        graph: graph,
        tickFormat: Rickshaw.Fixtures.Number.formatKMBT,
        ticksTreatment: ticksTreatment
    } );

    yAxis.render();

    var controls = new RenderControls( {
        element: document.querySelector('#chart-panel-' + viewid),
        graph: graph
    } );

    var event_listener = new EventSource("/views/" + viewid + "/data");
    event_listener.onmessage = function (e) {
        var data = JSON.parse(e.data);
        for (series of graph.series) {
            if (series.name === data.var) {
                last_data = series.data[series.data.length - 1];
                series.data.push({'x': last_data['x'] + 1, 'y': parseFloat(data.value)});
                if (series.data.length > 3000) {
                    series.data.shift();
                }
            }
        }
        graph.update();
    };

    var previewXAxis = new Rickshaw.Graph.Axis.Time({
        graph: preview.previews[0],
        timeFixture: new Rickshaw.Fixtures.Time.Local(),
        ticksTreatment: ticksTreatment
    });

    previewXAxis.render();
}

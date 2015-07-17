from __future__ import print_function

from flask import render_template
import threading

from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, cursession, push, output_server
from bokeh.embed import autoload_server

from devviz import redis_store as r

class BokehLinechart(object):
    def __init__(self, variables):
        self.script = ('<script src="http://cdn.pydata.org/bokeh/release/'
                       'bokeh-0.9.1.min.js"></script>')
        self.style = ('<link ref="stylesheet" type="text/css" '
                      'href="http://cdn.pydata.org/bokeh/release/'
                      'bokeh-0.9.1.min.css" />')
        self._updated = {}
        self._is_updated = threading.Event()
        self.variables = variables

    @property
    def content(self):
        plot, session = self.create_plot()
        divs = autoload_server(plot, session)

        thread = threading.Thread(target=self.update_plot,
                                  args=(plot, session))
        thread.start()


        return render_template('bokeh_linechart.html', divs=divs,
                               variables=self.variables)

    def update_plot(self, plot, session):
        subscriber = r.pubsub()
        subscriber.subscribe('y')
        for item in subscriber.listen():
            y = float(item['data'])
            renderer = plot.select(dict(name='line'))
            ds = renderer[0].data_source

            try:
                ds.data["x"].append(ds.data["x"][-1] + 1)
            except IndexError:
                ds.data['x'].append(0)
            ds.data["y"].append(y)

            if len(ds.data["x"]) > 100:
                ds.data["x"].pop(0)
                ds.data["y"].pop(0)

            session.store_objects(ds)

    def update(self, source_name):
        self._updated[source_name] = True
        self._is_updated.set()

    def create_plot(self):
        output_server('animation')
        source = ColumnDataSource(data=dict(x=[], y=[]))
        p = figure(plot_width=800, plot_height=400)
        p.line(x='x', y='y', source=source, name='line')
        push()
        return p, cursession()



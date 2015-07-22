__author__ = 'johannes'

from devviz import data_handler, app
from devviz.utils import sse_route

from collections import namedtuple

from flask import jsonify, session
import json
import time

Variable = namedtuple("Variable", ("name", "type", "value"))
Variable.__new__.__defaults__ = (None,)


class View(object):
    script = ''
    style = ''

    def __init__(self, variables=None, viewid=None):
        if variables is None:
            variables = []

        if viewid is None:
            self.viewid = data_handler.get_new_viewid()
            for var in variables:
                data_handler.add_view_var(self.viewid, var)

        else:
            self.viewid = viewid

    def add_var(self, variable):
        data_handler.add_view_var(self.viewid, variable)
        return jsonify({'content': self.content})

    def del_var(self, variable):
        data_handler.del_view_var(self.viewid, variable)
        return jsonify({'content': self.content})

    @property
    def variables(self):
        return [Variable(var, data_handler.get_type(var),
                         data_handler.get_value(var))
                for var in data_handler.get_view_vars(self.viewid)]


@app.route("/views/new/<name>")
def new_view(name):
    view = app.views[name]()
    data_handler.set_view(view.viewid, view)
    session['active_views'].append(view.viewid)
    return jsonify({"content": view.content})


@app.route("/views/<viewid>/add/<var>")
def add_var(viewid, var):
    view = data_handler.get_view(viewid)
    return view.add_var(var)


@app.route("/views/<viewid>/del/<var>")
def del_var(viewid, var):
    view = data_handler.get_view(viewid)
    return view.del_var(var)


@app.route("/views/<viewid>/data")
@sse_route
def data_stream(viewid):
    while True:
        time.sleep(.1)
        for var in data_handler.get_view_vars(viewid):
            yield json.dumps({"value": data_handler.get_value(var),
                              "var": var})



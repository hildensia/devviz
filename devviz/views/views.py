# -*- coding: utf-8 -*-
"""
    Views are the central module to implement views of data. The API is not yet
    stable.
"""
__author__ = 'Johannes Kulick'

from devviz import data_handler, app
from devviz.utils import sse_route

from collections import namedtuple

from flask import jsonify, session
from flask.views import MethodView
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


class ViewAPI(MethodView):
    def post(self, name):
        view = app.views[name]()
        data_handler.set_view(view.viewid, view)
        session['active_views'].append(view.viewid)
        return jsonify({"content": view.content})

    def delete(self, viewid):
        data_handler.del_view(viewid)
        session['active_views'].remove(viewid)
        return jsonify({"content": "true"})

    def get(self, viewid):
        view = data_handler.get_view(viewid)
        return jsonify({"content": view.content})


view_view = ViewAPI.as_view("views")
app.add_url_rule("/views/<int:viewid>", view_func=view_view,
                 methods=['DELETE', 'GET'])
app.add_url_rule("/views/<name>", view_func=view_view,
                 methods=['POST'])


class VariableAPI(MethodView):
    def post(self, viewid, var):
        view = data_handler.get_view(viewid)
        return view.add_var(var)

    def delete(self, viewid, var):
        view = data_handler.get_view(viewid)
        return view.del_var(var)

    def get(self, viewid, var):
        if var is None:
            view = data_handler.get_view(viewid)
            return jsonify({'variables': view.variables})
        else:
            return jsonify({'variables': Variable(var,
                                                  data_handler.get_type(var),
                                                  data_handler.get_value(var))
                            })


variable_view = VariableAPI.as_view("vars")
app.add_url_rule("/views/<int:viewid>/<var>", view_func=variable_view,
                 methods=['POST', 'DELETE', 'GET'])
app.add_url_rule("/views/<int:viewid>/vars", defaults={'var': None},
                 view_func=variable_view, methods=['GET'])


@app.route("/views/<int:viewid>/data")
@sse_route
def data_stream(viewid):
    while True:
        time.sleep(.1)
        for var in data_handler.get_view_vars(viewid):
            yield json.dumps({"value": data_handler.get_value(var),
                              "var": var})



__author__ = 'johannes'
from flask import render_template, jsonify, url_for
from devviz import data_handler, app
from devviz.utils import sse_route
from devviz.views import View, Variable
import json
import time


@app.route('/variables/stream')
@sse_route
def variables_stream():
    while True:
        vars = [{"name": var,
                 "type": data_handler.get_type(var)}
                for var in data_handler.get_variables()]
        yield json.dumps({"data": vars})
        time.sleep(.1)


@app.route('/variables')
def variables():
    vars = [{"name": var,
             "type": data_handler.get_type(var)}
            for var in data_handler.get_variables()]
    return jsonify({"data": vars})


class VariablesView(View):
    with app.app_context():
        script = ('<script src="https://cdnjs.cloudflare.com/ajax/libs/react/'
                  '0.13.3/react.js"></script>\n'
                  '<script src="{}"></script>\n'
                  .format(url_for('static', filename='js/variablesview.js')))
    url = 'variables'
    name = 'Variables'

    def __init__(self, variables=None, viewid=None):
        super(VariablesView, self).__init__(variables, viewid)

    @property
    def content(self):
        variables = data_handler.get_variables()
        vars = [Variable(name=var, type=data_handler.get_type(var))
                for var in variables]

        return render_template("variables.html", variables=vars,
                               viewid=self.viewid)


app.views[VariablesView.url] = VariablesView

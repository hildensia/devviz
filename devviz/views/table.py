__author__ = 'johannes'


from flask import render_template, request, Response, redirect
import time
from collections import namedtuple
from devviz import app, redis_store
from devviz.views import View
import json


Variable = namedtuple("Variable", ("name", "type", "value"))


@app.route('/table/stream/<viewid>')
def stream(viewid):
    if request.headers.get('accept') == 'text/event-stream':
        def events():
            while True:
                json_vars = redis_store.get("view-"+viewid)
                if json_vars is None:
                    continue
                variables = json.loads(json_vars)
                for var in variables:
                    value = redis_store.lindex(var, 0)
                    if value is None:
                        continue
                    varid = "#var-" + var
                    yield ('data: {{"varid": "{varid}", '
                           '"value": "{value}"}}\n\n'.
                           format(varid=varid, value=value))
                time.sleep(.1)
        return Response(events(), content_type='text/event-stream')
    return redirect("/")


class TableView(View):
    def __init__(self, variables=None, viewid=None):
        super(TableView, self).__init__(variables, viewid)
        self.style = """
        <style type="text/css">
        .tv-name{
            width: 20%;
        }
        .tv-type{
            width: 20%;
        }
        .tv-value{
            width: 60%;
        }
        </style>
        """

        self.script = """
        <script type="text/javascript">
        var source = new EventSource("/table/stream/{viewid}");
        source.onmessage = function(event) {{
            data = JSON.parse(event.data);
            $(data.varid).text(data.value);
        }};
        </script>
        """.format(viewid=self.viewid)

    @property
    def content(self):
        vars = []
        for var in self.variables:
            datatype = redis_store.get('type_' + var)
            value = redis_store.lindex(var, 0)
            vars.append(Variable(var, datatype, value))
        return render_template("table.html",
                               variables=vars,
                               viewid=self.viewid)


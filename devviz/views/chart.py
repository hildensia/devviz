__author__ = 'johannes'

from devviz import app
from devviz.views import View
from flask import render_template


class ChartView(View):
    url = 'chart'
    name = 'Charts and Plots'

    script = """
    <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.6/d3.min.js" charset="utf-8"></script>
    <script src="https://code.jquery.com/ui/1.11.3/jquery-ui.min.js"></script>
    <script src="/static/rickshaw/rickshaw.js"> </script>
    """

    style = """
    <link type="text/css" rel="stylesheet" href="static/rickshaw/rickshaw.css">
    <link type="text/css" rel="stylesheet" href="static/css/chartview.css">
    <link type="text/css" rel="stylesheet" href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/themes/base/jquery-ui.css">
    """

    def __init__(self, variables=None, viewid=None):
        super(ChartView, self).__init__(variables=variables, viewid=viewid)

    @property
    def content(self):
        return render_template("chart.html", variables=self.variables,
                               viewid=self.viewid)

app.views[ChartView.url] = ChartView

__author__ = 'johannes'

from devviz import app
from devviz.views import View

from flask import render_template


class TableView(View):
    style = """<style type="text/css">
        .tv-name{
            width: 20%;
        }
        .tv-type{
            width: 20%;
        }
        .tv-value{
            width: 60%;
        }
        </style>"""

    url = 'table'
    name = 'TableView'

    def __init__(self, variables=None, viewid=None):
        super(TableView, self).__init__(variables, viewid)

    @property
    def content(self):
        return render_template("table.html",
                               variables=self.variables,
                               viewid=self.viewid)


app.views[TableView.url] = TableView


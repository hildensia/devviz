__author__ = 'johannes'
from flask import render_template
from .views import BokehLinechart, VariablesView, TableView
from devviz import app


@app.route('/')
def main_page():
    return render_template("devviz.html",
                           views=[VariablesView(),
                                  TableView(variables=['y', 'z']),
                                  BokehLinechart(['y'])])

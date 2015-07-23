__author__ = 'johannes'
from flask import render_template, session
from devviz import app, data_handler
from devviz.views import VariablesView


@app.route('/')
def main_page():
    try:
        active_views = session['active_views']
    except KeyError:
        session['active_views'] = []
        active_views = []
    views = app.views.values()
    return render_template("devviz.html", views=views,
                           active_views=[VariablesView()] +
                                        [data_handler.get_view(viewid)
                                         for viewid in active_views])

__author__ = 'johannes'
from flask import render_template
from devviz import redis_store
from collections import namedtuple

Variable = namedtuple("Variable", ("name", "type"))


class VariablesView(object):
    def __init__(self):
        self.style = ''
        self.script = ''

    @property
    def content(self):
        variables = redis_store.lrange('variables', 0, -1)
        vars = []
        for var in variables:
            datatype = redis_store.get('type_' + var)
            vars.append(Variable(var, datatype))

        return render_template("variables.html",
                               variables=vars)



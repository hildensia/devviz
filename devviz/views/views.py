__author__ = 'johannes'

from devviz import redis_store
import json


class View(object):
    def __init__(self, variables, viewid=None):
        if viewid is None:
            self.viewid = redis_store.incr('views')
            redis_store.set("view-"+str(self.viewid), json.dumps(variables))
            print("set")
            self.variables = variables

        else:
            self.viewid = viewid
            self.variables = redis_store.get(viewid)

    def __del__(self):
        redis_store.delete(self.viewid)
        redis_store.decr('views')


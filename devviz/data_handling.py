# -*- coding: utf-8 -*-
"""
    data_handling
    ~~~~~~~~~~~~~

    This module provides an interface to all data, which are not session based
    but still persistant over multiple requests.
"""

import redis
from devviz import app


class DataHandler:
    def __init__(self):
        self._r = redis.StrictRedis(decode_responses=True)
        self._r.flushdb()
        self._pubsub = self._r.pubsub()

    def get_variables(self):
        return self._r.lrange("variables", 0, -1)

    def get_type(self, variable):
        return self._r.get("type_{}".format(variable))

    def get_values(self, variable):
        return self._r.lrange(variable, 0, -1)

    def get_value(self, variable, idx=0):
        return self._r.lindex(variable, idx)

    def get_view_vars(self, viewid):
        return self._r.lrange("view-{}".format(viewid), 0, -1)

    def set_view(self, viewid, view):
        self._r.set("view_type_{}".format(viewid), view.url)

    def get_view(self, viewid):
        view_name = self._r.get("view_type_{}".format(viewid))
        return app.views[view_name](viewid=viewid)

    def del_view(self, viewid):
        self._r.delete("view_type_{}".format(viewid))
        self._r.delete("view-{}".format(viewid))

    def subscribe(self, var):
        self._pubsub.subscribe(var)

    def listen(self):
        return self._pubsub.listen()

    def add_view_var(self, viewid, var):
        self._r.lpush("view-{}".format(viewid), var)

    def del_view_var(self, viewid, var):
        self._r.lrem("view-{}".format(viewid), 0, var)

    def get_new_viewid(self):
        return self._r.incr("views")




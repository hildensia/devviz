Views
=====

How to write a view
~~~~~~~~~~~~~~~~~~~

.. warning::
   The API is not stable yet. Be aware of rapid changes!


Views are the objects, that render the actual data to html and send it to the
browser. Although writing one is pretty straight-forward, keep in mind that we
write a `flask <http://flask.pocoo.org>`_ app, with all glitches it might have.
Let's write a simple table view as MyView for now.

The python side looks like this::

    from devviz import app
    from devviz.views import View


    class MyView(View):
       url = 'myview'

       def __init__(self, variables=None, viewid=None):
           super(MyView, self).__init__(variables, viewid)

       @property
       def content(self):
           return render_template("my_template.html", vars=self.variables)

    # register view to the main app
    app.views[MyView.url] = MyView


What's happening here? First you have to inherit from ``deviz.view.View``. Be
sure to call the ``super()`` constructor! Also set the static field ``url`` to
a unique name of the view, where it will be createable under later. Don't
bother how, devviz takes care of that.

Second implement the ``content`` property, to what your view should actually
look like. You can use ``self.viewid`` and ``self.variables`` from ``View``.
The ``viewid`` is a unique id for each view. So if there will be multiple
``MyView``'s they keep distinguishable. The member ``self.variables`` contains
a list of variables the view is attached to (including the name, type and
latest value of the variable).

.. warning::
   Your view is only pseudo-persistant! We take care of the ``variables`` and
   ``viewid``, but if you want anything else to be persistent use the redis
   instance of devviz!

In the end we register our view to the app, such that it appears in the
'Add view' menu.

Your template looks like::

   {% extends 'view.html' %}
   {% block view_title %}My fancy view{% endblock %}
   {% block view_content %}
   <ul>
   {% for var in vars %}
   <li>{{ var.name }} = {{ var.value }}</li>
   {% endfor %}
   </ul>
   {% endblock %}

You have to template-inherit from 'view.html'. This is a
`jinja2 <http://jinja.pocoo.org>`_ thing. The 'view.html' contains a ``view_title``
and a ``view_content`` block. Everything else is simply jinja2.

Data updates
~~~~~~~~~~~~

To do a bit more useful stuff you need to get informed about current values of
the data. For each view there is a API registered, to catch the current data,
under ``/views/<viewid>/data``. You can use all the fancy AJAX technology to
catch these data. In fact you can also register an ``EventSource`` to that URL,
to get server sent events, whenever a new value arrives.

.. automodule:: devviz.views.views
   :members:

# devviz
A live data vizualization for development.

http://www.github.com/hildensia/devviz

This is early experimental stuff. Expect it to be buggy.

The idea behind it is that `print`-debugging is quite convenient very often.
But than after a while you have a really cluttered stdout. And parsing it by
your eyes doesn't work well after a while. It would be handy to have a tool that
reads the stdout for you and makes nice vizualizations of it. This is what
devviz should be. Right now it can visualize 1D numerical data as a line plot
and a table view.
It's basicallly a [tracer bullet](http://www.artima.com/intv/tracer.html).

### How does it work?
It captures stdout of any programm (via a pipe).
If this is in a particular JSON format (right now: if it contains a field
called 'value', one called 'name' and one called 'type'), it visualizes it
using various views. (euphemisim...)

Technically it consists of three things:

 * `dcollect.py` - A script that reads the output and saves it into a NoSQL database
 * [redis](http://www.redis.io) - The NoSQL database holding the data
 * `devviz` - The actual vizualizer based on flask and bokeh

### Setup

#### Requirements

* [flask](http://flask.pocoo.org) - The web framework devviz uses
* [bokeh](http://bokeh.pydata.org) - The plotting library used
* [redis](http://www.redis.io) - The NoSQL database to keep the data

You can install all the python modules (including flask and bokeh) needed by:

    pip install -r requirements.txt
    
Look at the [redis website](http://www.redis.io) how to get redis.

For now we have to start bokeh and redis by hand. It's unconvenient but easy:

    $ bokeh-server
    $ redis-server

Now you can run devviz:

    python devviz.py

Open a browser and goto http://localhost:5000. You should see the various views
without content. To visualize something try:

    python scripts/output.py | scripts/dcollect.py
    
    
You should see something like:

![Screenshot](https://lh3.googleusercontent.com/yx-6l5rvcYcDUe9H23CuAu9fOWzOKh0LN4Rmsb36aiE=w1536-h805-no)

If you want to visualize your own data, you have to print out a JSON dict with a
`'value'` member. E.g.:

    import json
    x = 0
    while True:
        x += 1
        data = {'value': x}
        print(json.dumps(data))

Pipe your output to devviz and your done.

### THIS IS A TRACER BULLET

Remember: This is a tracer bullet. It is in a very early stadium. Don't expect 
it to be useful, cool or anything. But if you like the idea, I'm happy to get 
issues at github.
    

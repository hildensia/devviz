# devviz
A live data vizualization for development.

http://www.github.com/hildensia/devviz

This is the draft of an idea. 
The idea behind it is that `print`-debugging is quite convenient very often.
But than after a while you have a really cluttered stdout. And parsing it by
your eyes doesn't work well after a while. It would be handy to have a tool that
reads the stdout for you and makes nice vizualizations of it. This is what
devviz should be. Right now it can visualize 1D numerical data as a line plot.
There is nothing fancy yet. It's just a [tracer bullet](http://www.artima.com/intv/tracer.html). 

### How does it work?
It captures stdout of any programm (via a pipe).
If this is in a particular JSON format (right now: if it contains a field
called 'value'), it visualizes it as a live updating line-plot.

### Setup

First install flask, the web framework devviz works with

    pip install -r requirements.txt

Now you can try

    python scripts/output.py | python devviz.py

Open a browser and goto http://localhost:5000. You should see a line plot.
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

Remember: This is a tracer bullet. It is the very first version that runs
whatsoever. Don't expect it to be useful, cool or anything. But if you like the
idea, I'm happy to get issues at github.
    

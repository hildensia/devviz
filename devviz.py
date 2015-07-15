from __future__ import print_function

from flask import Flask, render_template, request, Response, redirect
import multiprocessing
import time
import json
import sys
import os
# import gevent
# import gevent.monkey
# from gevent.pywsgi import WSGIServer
# gevent.monkey.patch_all()

app = Flask(__name__)
q = multiprocessing.Queue()
application = app


@app.route('/stream')
def stream():
    if request.headers.get('accept') == 'text/event-stream':
        def events():
            while True:
                yield "data: {}\n\n".format(q.get())
                time.sleep(.1)
        return Response(events(), content_type='text/event-stream')
    return redirect("/")


@app.route('/')
def hello_world():
    return render_template("scrolling.html")


def read_data(fileno):
    n = 0
    sys.stdin = os.fdopen(fileno)
    print("read stdin")
    for data in sys.stdin:
        try:
            print(data, end='')
            q.put(data)
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    fn = sys.stdin.fileno()
    p = multiprocessing.Process(target=read_data, args=(fn,))
    p.start()
    app.run(debug=True)
    # http_server = WSGIServer(('127.0.0.1', 8001), app)
    # http_server.serve_forever()

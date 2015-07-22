__author__ = 'johannes'

from flask import request, Response, redirect
from functools import wraps


def sse_route(function):
    '''
    A decorator that wraps a flask route to be a server-sent event stream.
    The decorated function has to yield json strings.
    :param function:
    :return:
    '''
    def yielding_function(*args, **kwargs):
        for value in function(*args, **kwargs):
            yield "data: {}\n\n".format(value)

    @wraps(function)
    def sse_function(*args, **kwargs):
        if request.headers.get('accept') == 'text/event-stream':
            return Response(yielding_function(*args, **kwargs),
                            content_type='text/event-stream')
        return next(yielding_function(*args, **kwargs))
    return sse_function

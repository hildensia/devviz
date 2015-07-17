#!/usr/bin/env python

from __future__ import print_function
import argparse
import sys
import redis
import json

__author__ = 'johannes'

def main(args):
    r = redis.StrictRedis(host=args.server, port=args.port, db=0)

    #  Socket to talk to server
    print("Connecting to redis server…")

    try:
        for line in sys.stdin:
            if not line.startswith("dvv: "):
                print(line, end='')
                continue
            msg = line[5:]
            data = json.loads(msg)
            if not r.exists(data['name']):
                print("Add new variable: {}".format(data['name']))
                r.lpush('variables', data['name'])
            r.set('type_' + data['name'], data['type'])
            r.lpush(data['name'], data['value'])
            r.publish(data['name'], data['value'])

            print(msg, end='')


    except KeyboardInterrupt:
        print("Ctrl-C. Shutdown dcollect.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server", help="The URI of the devviz server."
                                               "[Default = localhost]",
                        type=str, default="localhost")
    parser.add_argument("-p", "--port", help="The port of the devviz server. "
                                             "[Default = 6379]",
                        type=int, default=6379)
    args = parser.parse_args()
    main(args)

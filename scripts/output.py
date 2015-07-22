#!/usr/bin/env python

from __future__ import print_function

import numpy as np
import json
import time
import sys
__author__ = 'johannes'


def main():
    value = 0
    while True:
        try:
            value = np.random.normal(value, .01)
            output = {"name": "y",
                      "type": "double",
                      "value": value}
            print("dvv: {}".format(json.dumps(output)))
            sys.stdout.flush()
            b = np.random.uniform(0, 1) > .5
            output = {"name": "z",
                      "type": "bool",
                      "value": b}
            print("dvv: {}".format(json.dumps(output)))
            sys.stdout.flush()
            time.sleep(.1)

        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    main()

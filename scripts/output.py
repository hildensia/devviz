import math
import json
import time
__author__ = 'johannes'


def main():
    n = 1
    while True:
        try:
            x = math.radians(float(n))
            value = math.sin((1/x) * (1/(1-x)))
            n += 1
            output = {"name": "y",
                      "type": "double",
                      "value": value}
            print(json.dumps(output))
            time.sleep(.01)


        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    main()

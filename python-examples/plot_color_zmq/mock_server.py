#!/usr/bin/env python3
import zmq
import pickle
import time
import random

context = zmq.Context()
socket = context.socket(zmq.PUB)


class ColorSensor:
    def __init__(self):
        self.r = random.randint(0, 256)
        self.g = random.randint(0, 256)
        self.b = random.randint(0, 256)

    @property
    def raw(self):
        self.r = min(255, max(0, self.r + random.randint(-5, 5)))
        self.g = min(255, max(0, self.g + random.randint(-5, 5)))
        self.b = min(255, max(0, self.b + random.randint(-5, 5)))
        return self.r, self.g, self.b


sensor = ColorSensor()

topic = b'COLOR'


def main():

    socket.bind('tcp://0.0.0.0:5000')

    try:
        while True:
            data = dict(zip('rgb', sensor.raw))
            data['t'] = time.time()
            socket.send(topic + b' ' + pickle.dumps(data))
            time.sleep(0.001)

    except (KeyboardInterrupt, SystemExit):
        socket.close()
        print('Aborted')


if __name__ == '__main__':
    main()

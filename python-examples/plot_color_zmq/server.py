#!/usr/bin/env python3
import zmq
from ev3dev.ev3 import ColorSensor
import pickle
import time

context = zmq.Context()
socket = context.socket(zmq.PUB)

sensor = ColorSensor('1')

topic = b'COLOR'


def main():

    socket.bind('tcp://0.0.0.0:5000')

    try:
        while True:
            data = dict(zip('rgb', sensor.raw))
            data['t'] = time.time()
            socket.send(topic + b' ' + pickle.dumps(data))

    except (KeyboardInterrupt, SystemExit):
        socket.close()
        print('Aborted')


if __name__ == '__main__':
    main()

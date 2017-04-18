#!/usr/bin/env python3
import zmq


context = zmq.Context()
socket = context.socket(zmq.REP)


if __name__ == '__main__':
    socket.bind('tcp://0.0.0.0:5000')

    try:

        while True:
            req = socket.recv()
            socket.send_string('Hello World')

    except (KeyboardInterrupt, SystemExit):
        pass

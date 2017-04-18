#!/usr/bin/env python3
import zmq
from ev3dev.ev3 import ColorSensor

sensor = ColorSensor('1')

context = zmq.Context()
socket = context.socket(zmq.REP)


if __name__ == '__main__':
    socket.bind('tcp://0.0.0.0:5000')

    try:

        print('Ready')

        while True:
            req = socket.recv_string()

            if req == 'raw':
                data = {'success': True, 'raw': sensor.raw}

            elif req == 'color':
                data = {'success': True, 'color': sensor.color}

            elif req == 'reflected':
                data = {'success': True, 'reflected': sensor.reflected_light_intensity}

            elif req == 'ambient':
                data = {'success': True, 'ambient': sensor.ambient_light_intensity}

            elif req == 'all':
                data = {
                    'success': True,
                    'ambient': sensor.ambient_light_intensity,
                    'reflected': sensor.reflected_light_intensity,
                    'color': sensor.color,
                    'raw': sensor.raw,
                }

            else:
                data = {'success': False}

            socket.send_pyobj(data)

    except (KeyboardInterrupt, SystemExit):
        print('Aborted')

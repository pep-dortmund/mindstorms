# -*- ecoding: utf-8 -*-
'''
This Program just shows the sensor values of robot
It works for the TankBot configuration we used in the school
'''
from __future__ import print_function, division, unicode_literals
from ev3.ev3dev import Motor
from ev3.lego import GyroSensor, UltrasonicSensor, ColorSensor
from time import sleep

from blessings import Terminal
term = Terminal()


# Setup sensors
gyro = GyroSensor(port=4)
gyro.start_value = gyro.ang
sonic_sensor = UltrasonicSensor(port=3)
color_sensor = ColorSensor(port=1)

def print_sensor_values():
    angle = '{:5d}'.format(gyro.ang - gyro.start_value)
    distance = '{:3.1f}'.format(sonic_sensor.dist_cm)
    color = '{}'.format(color_sensor.colors[color_sensor.color])
    rgb = color_sensor.rgb

    print(term.move(0, 0) + '{:<10} = {:>5}°'.format('Winkel', angle))
    print(term.move(1, 0) + '{:<10} = {:>5} cm'.format('Abstand', distance))
    print(term.move(2, 0) + '{:<10} = {:<10}'.format('Farbe', color))
    print(term.move(3, 0) + '{:<10} = {:03d} {:03d} {:03d}'.format('RGB', *rgb))


if __name__ == '__main__':
    try:
        with term.fullscreen():
            while True:
                print_sensor_values()
                sleep(0.01)

    except KeyboardInterrupt, SystemExit:
        pass

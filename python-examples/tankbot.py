# -*- coding:utf-8 -*-
'''
This module provides the TankBot class as
programming interface for the robot we used in the school project.
'''
from __future__ import print_function, division
from ev3.ev3dev import Motor
from ev3.lego import ColorSensor, GyroSensor, UltrasonicSensor


class TankBot(object):
    def __init__(self):
        # setup the motors
        self.motor_left = Motor(port='B')
        self.motor_right = Motor(port='D')
        self.motors = (self.motor_left, self.motor_right)

        self._speed = 0

        # setup the sensors
        self.color_sensor = ColorSensor(port=1)
        self.ultrasonic_sensor = UltrasonicSensor(port=3)
        self.gyro_sensor = GyroSensor(port=4)

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        for motor in self.motors:
            motor.duty_cycle_sp = int(-value)
        self._speed = -value

    def turn_seconds(self, seconds, speed):
        self.motor_left.run_time_limited(seconds * 1000, speed)
        self.motor_right.run_time_limited(seconds * 1000, -speed)

    def run_seconds(self, seconds, speed=50):
        # the TankBot has the motors in backwards direction
        # so we multiply the speed by -1 so that a positivs speed
        # means to go forward
        self.motor_left.run_time_limited(seconds * 1000, -speed)
        self.motor_right.run_time_limited(seconds * 1000, -speed)

    def run_forever(self, speed=50):
        # the TankBot has the motors in backwards direction
        # so we multiply the speed by -1 so that a positivs speed
        # means to go forward
        self.motor_left.run_forever(-speed)
        self.motor_right.run_forever(-speed)

    def run_direct(self, speed=50):
        for motor in self.motors:
            motor.mode = 'run-direct'
            motor.duty_cycle_sp = -int(speed)
            motor.write_value('command', 'run-direct')

    def stop(self):
        self.motor_left.stop()
        self.motor_right.stop()


    # these two functions provide a context manager: with TankBot as bot:
    # it makes sure, that the motors are stopped on exiting the with statement
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.stop()

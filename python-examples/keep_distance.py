#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
In this example, we let the TankBot keep a
distance to a target.
'''
from __future__ import print_function, division
from tankbot import TankBot
from controller import PID


def keep_distance(bot, target_distance):
    speed = 0
    bot.run_direct(speed)
    controller = PID(
        setpoint=target_distance,
        func=lambda : bot.ultrasonic_sensor.dist_cm,
        kp=-5,
        ki=-2,
        kd=-0.5,
        tau=5,
        limits=[-100, 100]
    )
    while True:
        bot.speed = controller()


if __name__ == '__main__':
    try:
        with TankBot() as bot:
            keep_distance(bot, 20)
    except (KeyboardInterrupt, SystemExit):
        pass

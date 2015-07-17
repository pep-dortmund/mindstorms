#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
In this example, we let the TankBot keep a
distance to a target.
'''
from __future__ import print_function, division
from tankbot import TankBot


def keep_distance(bot, target_distance):
    speed = 0
    bot.run_direct(speed)
    while True:
        current_distance = bot.ultrasonic_sensor.dist_cm
        difference = current_distance - target_distance
        if difference > 0:
            speed = min(5*difference, 100)
        else:
            speed = max(200 * difference / target_distance, -100)
        bot.speed = speed


if __name__ == '__main__':
    try:
        with TankBot() as bot:
            keep_distance(bot, 10)
    except (KeyboardInterrupt, SystemExit):
        pass

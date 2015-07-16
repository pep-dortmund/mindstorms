#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
This script demonstrates how to use multithreading in
python to do several tasks (nearly) at once.
In this example, we let the TankBot turn fast from
left to right and back while simultaniously writing
the angle of the gyro sensor to a file.
'''
from __future__ import print_function, division
from tankbot import TankBot
from threading import Thread, Event
from datetime import datetime
from time import sleep


def wiggle_wiggle(bot, stop_event):
    '''
    This function is meant to run as thread.
    It just lets the bot wiggle by turning left and right fast.
    It stops stop_event.set() is called.
    '''
    while not stop_event.is_set():
        bot.turn_seconds(seconds=0.4, speed=50)
        stop_event.wait(0.4)
        bot.turn_seconds(seconds=0.4, speed=-50)
        stop_event.wait(0.4)


def save_angle(bot, outfilename, stop_event):
    '''
    This function is meant to run as thread.
    It writes a timestamp and the angle of the gyro
    to a csv-file <outfilename>.
    It stops stop_event.set() is called.
    '''
    with open(outfilename, 'w') as outfile:
        outfile.write('date,angle\n')
        while not stop_event.is_set():
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            angle = bot.gyro_sensor.ang
            outfile.write('{:s},{:d}\n'.format(now, angle))


if __name__ == '__main__':
    try:
        # we need an event, to be able to communicate to the threads
        # most important for shutting them down
        stop_event = Event()

        # The TankBot class has a context manager that stops
        # the motors on exiting the with block
        with TankBot() as bot:
            # create the Threads, args are handed over to the <target>-function
            move_thread = Thread(target=wiggle_wiggle,
                                 args=(bot, stop_event),
                                 )
            save_thread = Thread(target=save_angle,
                                 args=(bot, 'test.csv', stop_event),
                                 )

            # start the threads
            move_thread.start()
            save_thread.start()

            # this is needed to stay in the try except block
            # otherwise we could never terminate the program
            while True:
                sleep(10)
    except (KeyboardInterrupt, SystemExit):
        # on ctrl+c: stop the threads, then exit
        stop_event.set()

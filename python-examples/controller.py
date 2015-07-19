#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np


class PID(object):
    '''
    a proportional/integral/derivative controller
    See wikipedia: https://en.wikipedia.org/wiki/PID_controller
    '''
    def __init__(self, setpoint, func, kp, ki, kd, tau, limits):
        '''
        Parameters
        ----------
        setpoint : float
            the target value of your procees
        func : function
            a function that returns the current value of the process variable
        kp : float
            the weight for the proportianal term
        ki : float
            the weight for the integral term
        kd : float
            the weight for the differential term

        limits : 2-tuple
            value range for the return value
        '''

        self.setpoint = setpoint
        self.current_value = func

        self.kp = kp
        self.ki = ki
        self.tau = tau
        self.kd = kd

        self.last_errors = np.zeros(tau)

        self.limits = limits

    def __call__(self):
        error = self.setpoint - self.current_value()
        self.last_errors[:-1] = self.last_errors[1:]
        self.last_errors[-1] = error

        P = self.kp * error
        I = self.ki * self.last_errors.sum()
        D = self.kd * (self.last_errors[-1] - self.last_errors[-2])

        PID = P + I + D
        
        if PID < self.limits[0]:
            PID = self.limits[0]
        elif PID > self.limits[1]:
            PID = self.limits[1]

        return PID

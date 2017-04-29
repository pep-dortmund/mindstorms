#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np


class PID:
    '''
    a proportional/integral/derivative controller
    See wikipedia: https://en.wikipedia.org/wiki/PID_controller
    '''
    def __init__(
            self,
            setpoint,
            func,
            proportianal_weight,
            integral_weight,
            differantial_weight,
            tau,
            limits,
            ):
        '''
        Parameters
        ----------
        setpoint : float
            the target value of your procees
        func : function
            a function that returns the current value of the process variable
        proportianal_weight : float
            the weight for the proportianal term
        integral_weight : float
            the weight for the integral term
        differantial_weight : float
            the weight for the differential term
        tau : integer
            number of measurements to use for integral and
            mean of derivative
        limits : 2-tuple
            value range for the return value
        '''

        self.setpoint = setpoint
        self.current_value = func

        self.proportianal_weight = proportianal_weight
        self.integral_weight = integral_weight
        self.tau = tau
        self.differantial_weight = differantial_weight

        self.last_errors = np.zeros(tau)

        self.limits = limits

    def __call__(self):
        error = self.setpoint - self.current_value()
        self.last_errors[:-1] = self.last_errors[1:]
        self.last_errors[-1] = error

        P = self.proportianal_weight * error
        I = self.integral_weight * self.last_errors.sum()
        D = self.differantial_weight * np.mean(np.diff(self.last_errors))

        PID = P + I + D

        if PID < self.limits[0]:
            PID = self.limits[0]

        elif PID > self.limits[1]:
            PID = self.limits[1]

        return PID

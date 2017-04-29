from ev3dev import ev3
import code
from controller import PID
import time
from threading import Thread, Event


class GyroBoy:

    def __init__(
            self,
            left_motor_port='outD',
            right_motor_port='outA',
            arm_motor_port='outB',
            color_port='in1',
            gyro_port='in2',
            touch_port='in3',
            ultrasonic_port='in4',
            ):

        self.left_motor = ev3.LargeMotor(left_motor_port)
        self.right_motor = ev3.LargeMotor(right_motor_port)
        self.arm_motor = ev3.MediumMotor(arm_motor_port)
        self.touch_sensor = ev3.TouchSensor(touch_port)
        self.gyro = ev3.GyroSensor(gyro_port)
        self.color_sensor = ev3.ColorSensor(color_port)
        self.distance_sensor = ev3.UltrasonicSensor(color_port)

        self.hold_thread = None
        self.duty_cycle_sp = 0
        self.calibrate_gyro()

        self.pid = PID(
            setpoint=self.gyro.angle,
            func=lambda: self.gyro.angle,
            proportianal_weight=-25,
            integral_weight=0,
            differantial_weight=0,
            tau=10,
            limits=[-100, 100],
        )

        self.motors = {
            'left': self.left_motor,
            'right': self.right_motor,
            'arm': self.arm_motor,
        }
        for m in self.motors.values():
            m.reset()

        self.button_thread = self.ButtonThread(self)
        self.button_thread.start()

    def __exit__(self, exc_type, exc_value, traceback):
        for m in self.motors.values():
            self.stop_hold()
            self.button_thread.terminate()
            m.stop()
            m.reset()

    def __enter__(self):
        return self

    def calibrate_gyro(self):
        self.gyro.mode = self.gyro.MODE_GYRO_RATE
        time.sleep(0.1)
        self.gyro.mode = self.gyro.MODE_GYRO_ANG

    @property
    def duty_cycle_sp(self):
        return self.duty_cycle_sp

    @duty_cycle_sp.setter
    def duty_cycle_sp(self, new_val):
        self.left_motor.duty_cycle_sp = new_val
        self.right_motor.duty_cycle_sp = new_val

    def start_hold(self):
        if self.hold_thread is None:
            self.hold_thread = self.HoldThread(self)
            self.hold_thread.start()

    def stop_hold(self):
        if self.hold_thread is not None:
            self.hold_thread.terminate()
            self.hold_thread = None

    def toggle_hold(self):
        if self.hold_thread is None:
            self.start_hold()
        else:
            self.stop_hold()

    class HoldThread(Thread):
        def __init__(self, bot):
            super().__init__()
            self.event = Event()
            self.bot = bot
            self.motors = (self.bot.left_motor, self.bot.right_motor)

        def run(self):
            for m in self.motors:
                m.duty_cycle_sp = 0
                m.run_direct()

            while not self.event.is_set():
                new_val = self.bot.pid()
                self.bot.duty_cycle_sp = new_val

        def terminate(self):
            for m in self.motors:
                m.stop_action = m.STOP_ACTION_BRAKE
                m.stop()
            self.event.set()

    class ButtonThread(Thread):
        def __init__(self, bot):
            super().__init__()
            self.event = Event()
            self.bot = bot

        def run(self):
            while not self.event.is_set():
                if self.bot.touch_sensor.is_pressed:
                    self.bot.toggle_hold()
                    self.event.wait(0.5)

        def terminate(self):
            self.event.set()


if __name__ == '__main__':
    with GyroBoy() as bot:
        code.interact(local=locals())

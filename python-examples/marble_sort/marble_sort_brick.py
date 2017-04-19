from ev3dev.ev3 import MediumMotor, ColorSensor
from argparse import ArgumentParser
import time

parser = ArgumentParser()
parser.add_argument('-m', '--motor-port', default='A')
parser.add_argument('-s', '--sensor-port', default='1')


class MarbleSorter:

    def __init__(self, motor_port, sensor_port):
        self.motor = MediumMotor(motor_port)
        self.sensor = ColorSensor(sensor_port)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.motor.stop()
        self.motor.reset()

    def eject(self, speed=0.3):
        self.motor.stop()
        self.motor.reset()
        self.motor.stop_action = self.motor.STOP_ACTION_HOLD
        self.motor.position_sp = -120
        self.motor.speed_sp = int(speed * self.motor.max_speed)
        self.motor.run_to_rel_pos()
        self.motor.wait_until('holding', timeout=2000)

    def run_motor(self, speed=0.3):
        self.motor.reset()
        self.motor.speed_sp = int(speed * self.motor.max_speed)
        self.motor.run_forever()

    def stop(self):
        self.motor.stop()


def main():

    args = parser.parse_args()

    print('Starting')
    with MarbleSorter(args.motor_port, args.sensor_port) as sorter:

        while True:
            sorter.eject()
            sorter.run_motor()
            time.sleep(5)


if __name__ == '__main__':
    main()

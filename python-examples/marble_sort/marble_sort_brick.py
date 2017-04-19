from ev3dev.ev3 import MediumMotor, ColorSensor
from argparse import ArgumentParser
import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)

parser = ArgumentParser()
parser.add_argument('server')
parser.add_argument('-p', '--port', type=int, default=5000)
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

    def eject(self, speed=0.3):
        self.motor.stop()
        self.motor.stop_action = self.motor.STOP_ACTION_HOLD
        self.motor.position_sp = -120
        self.motor.speed_sp = int(speed * self.motor.max_speed)
        self.motor.run_to_rel_pos()
        self.motor.wait_until('holding', timeout=2000)

    def run_motor(self, speed=0.3):
        self.motor.speed_sp = int(speed * self.motor.max_speed)
        self.motor.run_forever()

    def stop(self):
        self.motor.stop()

    @property
    def empty(self):
        return all((
            33 < self.sensor.red < 43,
            22 < self.sensor.green < 32,
            59 < self.sensor.blue < 69,
        ))

    def measure(self, num_values, interval=0.01):
        self.run_motor()
        values = []
        for i in range(num_values):
            values.append(dict(zip('rgb', self.sensor.raw)))
            time.sleep(interval)

        self.stop()
        return values


def main():

    args = parser.parse_args()

    socket.connect('tcp://{}:{}'.format(args.server, args.port))

    print('Starting')
    with MarbleSorter(args.motor_port, args.sensor_port) as sorter:

        while True:
            while sorter.empty:
                time.sleep(0.1)

            time.sleep(0.2)
            t0 = time.perf_counter()
            color_values = sorter.measure(100)
            socket.send_pyobj(color_values)
            socket.recv()
            t1 = time.perf_counter()
            print('Sending values took {} seconds'.format(t1 - t0))

            sorter.eject()
            time.sleep(0.5)


if __name__ == '__main__':
    main()

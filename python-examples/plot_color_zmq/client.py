import matplotlib.pyplot as plt
import zmq
import pickle
from argparse import ArgumentParser
import numpy as np
import time

parser = ArgumentParser()
parser.add_argument('host')
parser.add_argument('-p', '--port', type=int, default=5000)
parser.add_argument('--topic', default=b'COLOR', type=bytes)
parser.add_argument('--buffer', default=5, type=int)
parser.add_argument('--points', default=250, type=int)

context = zmq.Context()
socket = context.socket(zmq.SUB)


def main():
    args = parser.parse_args()
    t0 = time.time()

    socket.subscribe(args.topic)
    socket.connect('tcp://{}:{}'.format(args.host, args.port))

    plt.ion()

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_ylim(0, 256)

    plot_data = {k: np.full(args.points, np.nan) for k in 'trgb'}
    plot_lines = {k: ax.plot([], [], k)[0] for k in 'rgb'}

    fig.show()

    while True:

        for i in range(args.buffer):
            raw_data = socket.recv().lstrip(args.topic + b' ')
            data = pickle.loads(raw_data)

            plot_data['t'][:-1] = plot_data['t'][1:]
            plot_data['t'][-1] = data['t'] - t0

            for key in 'rgb':
                plot_data[key][:-1] = plot_data[key][1:]
                plot_data[key][-1] = data[key]

        for key in 'rgb':
            plot_lines[key].set_ydata(plot_data[key])
            plot_lines[key].set_xdata(plot_data['t'])

        ax.set_xlim(np.nanmin(plot_data['t']), np.nanmax(plot_data['t']))
        fig.canvas.draw()
        fig.canvas.flush_events()


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        socket.close()

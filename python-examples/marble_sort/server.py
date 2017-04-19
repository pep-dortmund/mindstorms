from argparse import ArgumentParser
import matplotlib.pyplot as plt
import zmq

parser = ArgumentParser()
parser.add_argument('-p', '--port', type=int, default=5000)

context = zmq.Context()
socket = context.socket(zmq.REP)


def main():
    args = parser.parse_args()
    socket.bind('tcp://0.0.0.0:{}'.format(args.port))

    plt.ion()
    fig, ax = plt.subplots()
    fig.show()

    while True:
        data = socket.recv_pyobj()
        socket.send_string('ok')

        r = [c['r'] for c in data]
        g = [c['g'] for c in data]
        b = [c['b'] for c in data]

        ax.cla()
        ax.plot(r, 'r')
        ax.plot(g, 'g')
        ax.plot(b, 'b')
        ax.set_ylim(0, 256)

        fig.canvas.draw()
        fig.canvas.flush_events()


if __name__ == '__main__':
    main()

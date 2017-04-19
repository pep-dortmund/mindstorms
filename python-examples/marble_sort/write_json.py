from argparse import ArgumentParser
import zmq
import json

parser = ArgumentParser()
parser.add_argument('outputfile')
parser.add_argument('-p', '--port', type=int, default=5000)

context = zmq.Context()
socket = context.socket(zmq.REP)


def main():
    args = parser.parse_args()
    socket.bind('tcp://0.0.0.0:{}'.format(args.port))

    events = 0
    with open(args.outputfile, 'a') as f:
        while True:
            data = socket.recv_pyobj()
            socket.send_string('ok')

            events += 1
            print('Events:', events)

            f.write(json.dumps(data))
            f.write('\n')


if __name__ == '__main__':
    main()

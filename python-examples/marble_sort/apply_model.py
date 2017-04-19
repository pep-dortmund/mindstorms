from argparse import ArgumentParser
import zmq
from sklearn.externals import joblib
from feature_generation import feature_generation
import numpy as np

parser = ArgumentParser()
parser.add_argument('model')
parser.add_argument('-p', '--port', type=int, default=5000)

context = zmq.Context()
socket = context.socket(zmq.REP)


def main():
    args = parser.parse_args()
    socket.bind('tcp://0.0.0.0:{}'.format(args.port))

    model = joblib.load(args.model)

    while True:
        data = socket.recv_pyobj()
        socket.send_string('ok')

        features = feature_generation(data)

        X = np.array([[features[f] for f in model.features]])

        pred = model.predict(X)
        print(model.labels[pred[0]])


if __name__ == '__main__':
    main()

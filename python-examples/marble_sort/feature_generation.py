import json
import numpy as np
from argparse import ArgumentParser
import pandas as pd

parser = ArgumentParser()
parser.add_argument('inputfile')
parser.add_argument('outputfile')


def feature_generation(event):
    row = {}
    arrays = {}
    for color in 'rgb':
        arrays[color] = np.array([c[color] for c in event])

    for color in 'rgb':
        row[color + '_mean'] = np.mean(arrays[color])
        row[color + '_std'] = np.std(arrays[color])
        row[color + '_min'] = np.min(arrays[color])
        row[color + '_max'] = np.max(arrays[color])

        for p in np.arange(5, 100, 5):
            row[color + '_p{}'.format(p)] = np.percentile(arrays[color], p)

    return row


def main():

    args = parser.parse_args()

    with open(args.inputfile) as f:
        data = list(map(json.loads, f))

    rows = []
    for event in data:
        rows.append(feature_generation(event))

    pd.DataFrame(rows).to_csv(args.outputfile, index=False)


if __name__ == '__main__':
    main()

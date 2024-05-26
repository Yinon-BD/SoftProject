import sklearn.metrics as metrics
import numpy as np
import pandas as pd
import sys

if __name__ == '__main__':
    arguments = sys.argv[1:]
    k = int(arguments[0])
    filename = arguments[1]

    data = pd.read_csv(filename, header=None)
    N = len(data)
    d = len(data.columns)

    
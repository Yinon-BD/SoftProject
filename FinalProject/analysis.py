import sklearn.metrics as metrics
import numpy as np
import pandas as pd
from kmeans import fit as kfit
from symnmf import function_hub as sfit
import sys

if __name__ == '__main__':
    arguments = sys.argv[1:]
    k = int(arguments[0])
    filename = arguments[1]
    max_iter = 200
    epsilon = 0.001

    data = pd.read_csv(filename, header=None)
    N = len(data)
    d = len(data.columns)
    data = data.values.tolist()
    kmeansSil = metrics.silhouette_score(data, kfit(N, k, data, max_iter, epsilon))
    symSil = metrics.silhouette_score(data, sfit(data, N, d, k, "symnmf"))
    
    print(f"nmf: {kmeansSil}")
    print(f"kmeans: {symSil}")
    
    
    
    
    
    
    

    
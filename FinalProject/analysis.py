import sklearn.metrics as metrics
import numpy as np
import pandas as pd
from kmeans import fit as kfit
from symnmf import function_hub as sfit
import sys

def process_nmf_res(H):
    res = [np.argmax(row) for row in H]
    return res
        

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
    kmeansSil = metrics.silhouette_score(data, kfit(N, d, k, data, max_iter, epsilon)[1])
    nmfSil = metrics.silhouette_score(data, process_nmf_res(sfit(data, N, d, k, "symnmf")))
    
    print(f"nmf: {format(nmfSil, '.4f')}")
    print(f"kmeans: {format(kmeansSil, '.4f')}")
    
    
    
    
    
    
    

    
import sys
import numpy as np
import pandas as pd
import mysymnmf

np.random.seed(0)

def read_data_points(file_path):
    return pd.read_csv(file_path, header=None)


def initialize_matrix(dps, N, d, k):
    W = mysymnmf.norm(dps, N, d)
    m = np.mean(np.array(W))
    H = np.random.uniform(0, 2*np.sqrt(m/k), (N, k))
    H_list = H.tolist()
    return H_list, W

def function_hub(dps, N, d, k, goal):
    if goal == "sym":
        return mysymnmf.sym(dps, N, d)

    elif goal == "ddg":
        return mysymnmf.ddg(dps, N, d)

    elif goal == "norm":
        return mysymnmf.norm(dps, N, d)

    elif goal == "symnmf":
        init_mat, W = initialize_matrix(dps, N, d, k)
        return mysymnmf.symnmf(W, N, d, k, init_mat)

    else:
        print("An Error Has Occurred.")
        sys.exit()

def print_result(result): # printing the result elements separated by a comma
    for i in range(len(result)):
        print(",".join([format(result[i][j], ".4f") for j in range(len(result[i]))]))

if __name__ == '__main__':

    arguments = sys.argv[1:]
    k = int(arguments[0])
    goal = arguments[1]
    file_name = arguments[2]
    dps_df = read_data_points(file_name)
    N = len(dps_df)
    d = len(dps_df.columns)
    dps = dps_df.values.tolist()

    result = function_hub(dps, N, d, k, goal)

    print_result(result)
    
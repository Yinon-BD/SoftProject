import sys
import numpy as np
import pandas as pd
import mykmeanssp


def euclidean_distance(vector1, vector2):
    distance = 0
    for i in range(len(vector1)):
        distance += (vector1[i] - vector2[i]) ** 2
    distance **= 0.5
    return distance


def centroids_initialization(vectors, k, N):
    centroids = []
    dp2c = [-1] * N
    indice_list = []
    vectors_copy = vectors.copy()
    chosen_idx = np.random.choice(N)
    centroids.append(vectors.iloc[chosen_idx].values)
    dp2c[chosen_idx] = 0
    indice_list.append(chosen_idx)
    vectors_copy.drop([chosen_idx])
    while len(centroids) < k:
        distances = []
        for i in range(len(vectors_copy)):
            distances.append(min([euclidean_distance(vectors_copy.iloc[i].values, centroids[j]) for j in range(len(centroids))]))
        distances = np.array(distances)
        probabilities = distances / distances.sum()
        chosen_idx = np.random.choice(N, p=probabilities)
        centroids.append(vectors_copy.iloc[chosen_idx].values)
        dp2c[chosen_idx] = len(centroids) - 1
        indice_list.append(chosen_idx)
        vectors_copy.drop([chosen_idx])
    return centroids, dp2c, indice_list


if __name__ == '__main__':
    np.random.seed(0)

    arguments = sys.argv[1:]

    if not (len(arguments) == 4 or len(arguments) == 5):
        print("An Error Has Occurred")
        sys.exit()
    if not (arguments[0].isdigit() and int(arguments[0]) > 1):
        print("Invalid number of clusters!")
        sys.exit()
    if len(arguments) == 5:
        if not (arguments[1].isdigit() and int(arguments[1]) > 1 and int(arguments[1]) < 1000):
            print("Invalid maximum iteration!")
            sys.exit()
        max_iter = int(arguments[1])  # current run constants
        try:
            epsilon = float(arguments[2])
            if epsilon < 0:
                print("Invalid epsilon!")
                sys.exit()
        except ValueError:
            print("Invalid epsilon!")
            sys.exit()
        filename1 = arguments[3]
        filename2 = arguments[4]
    elif len(arguments) == 4:
        max_iter = 300
        try:
            epsilon = float(arguments[1])
            if epsilon < 0:
                print("Invalid epsilon!")
                sys.exit()
        except ValueError:
            print("Invalid epsilon!")
            sys.exit()
        filename1 = arguments[2]
        filename2 = arguments[3]

    df1 = pd.read_csv(filename1, index_col=[0], header=None)
    df2 = pd.read_csv(filename2, index_col=[0], header=None)
    vectors = pd.merge(df1, df2, left_index=True, right_index=True, how='inner', sort=True)  # inner join

    vectors.columns = [i for i in range(len(vectors.columns))]  # rename columns by element index

    d = len(vectors.columns)
    k = int(arguments[0])  # current run constants
    eps = 0
    N = len(vectors)
    if k >= N:
        print("Invalid number of clusters!")
        sys.exit()
    centroids, dp2c, indice_list = centroids_initialization(vectors, k, N)
    # convert centroids entries to lists:
    centroids = [list(centroids[i]) for i in range(len(centroids))]
    vecotrs_list = vectors.values.tolist()    
    
    # KMeans
    centroids_from_kmeans = mykmeanssp.fit(vecotrs_list, centroids, dp2c, k, N, d, max_iter, eps)
    for i in range(len(indice_list)):
        if i != (len(indice_list) - 1):
            print(indice_list[i], end=",")
        else:
            print(indice_list[i])
    for centroid in centroids_from_kmeans:
        print(','.join([format(centroid[j], ".4f") for j in range(len(centroid))]))



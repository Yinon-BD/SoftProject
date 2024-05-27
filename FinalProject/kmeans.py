import sys

def euclidean_distance(vector1, vector2):
    distance = 0
    for i in range(len(vector1)):
        distance += (vector1[i] - vector2[i]) ** 2
    distance **= 0.5
    return distance


def calculate_mean(centroid, dimension):  # calculate new mean
    totals = [0 for _ in range(dimension)]
    for vector in centroid:
        for i in range(dimension):
            totals[i] += vector[i]
    return tuple([totals[i] / len(centroid) for i in range(len(totals))])

def error_checking(arguments):
    assert len(arguments) == 4 or len(arguments) == 5, "An Error Has Occurred"
    assert arguments[0].isdigit() and int(arguments[0]) > 1, "Invalid number of clusters!"
    assert arguments[1].isdigit() and int(arguments[1]) > 1, "Invalid number of points"
    assert int(arguments[0]) < int(arguments[1]), "Invalid number of clusters!"
    assert arguments[2].isdigit() and int(arguments[2]) > 0, "invalid dimension of point!"


def fit(N, d, k, vectors, max_iter, epsilon):
    centroids = []  # list of centroids' list
    centroids_means = []  # list of centroids' means
    vectors_location = [-1 for _ in range(N)]
    for i in range(k):
        centroids.append([vectors[i]])
        centroids_means.append(vectors[i])
        vectors_location[i] = i

    for i in range(max_iter):
        below_epsilon = True
        for j in range(N):
            if i == 0 and (j < k):
                continue
            distances = []
            for l in range(k):
                distances.append(euclidean_distance(vectors[j], centroids_means[l]))
            closest = distances.index(min(distances))
            if vectors_location[j] != closest and vectors_location[j] != -1:
                centroids[vectors_location[j]].remove(vectors[j])
            if vectors_location[j] != closest:
                centroids[closest].append(vectors[j])
            vectors_location[j] = closest
        for j in range(k):
            new_mean = calculate_mean(centroids[j], d)
            if euclidean_distance(new_mean, centroids_means[j]) >= epsilon:
                below_epsilon = False
            centroids_means[j] = new_mean
        if below_epsilon:
            break
    return centroids_means, vectors_location

def print_results(centroids_means, dimension):
    for i in range(len(centroids_means)):
        for j in range(dimension):
            if j == dimension - 1:
                print(round(centroids_means[i][j], 4))
            else:
                print(round(centroids_means[i][j], 4), end=",")

if __name__ == '__main__':
    arguments = sys.argv[1:]
    error_checking(arguments)

    if len(arguments) == 5:
        assert arguments[3].isdigit() and int(arguments[3]) > 0 and int(arguments[3]) < 1000, "Invalid maximum iteration!"
        max_iter = int(arguments[3])  # current run constants
        try:
            f = open(arguments[4], "r")
        except IOError:
            print("An Error Has Occurred")
            sys.exit()
    elif len(arguments) == 4:
        max_iter = 200  # current run constants
        try:
            f = open(arguments[3], "r")
        except IOError:
            print("An Error Has Occurred")
            sys.exit()

    vectors = []
    for line in f:
        vectors.append(line)
    for i in range(len(vectors)):
        vectors[i] = tuple(map(float, vectors[i].split(',')))

    dimension = len(vectors[0])
    k = int(arguments[0])  # current run constants
    epsilon = 0.001  # current run constants
    N = int(arguments[1])  # current run constants
    d = int(arguments[2])  # current run constants

    centroids_means, vectors_location = fit(N, d, k, vectors, max_iter, epsilon)

    print_results(centroids_means, dimension)
    
    f.close()

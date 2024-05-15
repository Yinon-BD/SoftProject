import sys

arguments = sys.argv[1:]

assert len(arguments) == 4 or len(arguments) == 5, "An Error Has Occurred"
assert arguments[0].isdigit() and int(arguments[0]) > 1, "Invalid number of clusters!"
assert arguments[1].isdigit() and int(arguments[1]) > 1, "Invalid number of points"
assert int(arguments[0]) < int(arguments[1]), "Invalid number of clusters!"
assert arguments[2].isdigit() and int(arguments[2]) > 0, "invalid dimension of point!"
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
centroids = []  # list of centroids' list
centroids_means = []  # list of centroids' means
vectors_location = [-1 for i in range(len(vectors))]
for i in range(k):
    centroids.append([vectors[i]])
    centroids_means.append(vectors[i])
    vectors_location[i] = i


def euclidean_distance(vector1, vector2):
    distance = 0
    for i in range(len(vector1)):
        distance += (vector1[i] - vector2[i]) ** 2
    distance **= 0.5
    return distance


def calculate_mean(centroid):  # calculate new mean
    totals = [0 for _ in range(dimension)]
    for vector in centroid:
        for i in range(dimension):
            totals[i] += vector[i]
    return tuple([totals[i] / len(centroid) for i in range(len(totals))])


for i in range(max_iter):
    below_epsilon = True
    for j in range(len(vectors)):
        if i == 0 and (j < k):
            continue
        distances = []
        for l in range(len(centroids)):
            distances.append(euclidean_distance(vectors[j], centroids_means[l]))
        closest = distances.index(min(distances))
        if vectors_location[j] != closest and vectors_location[j] != -1:
            centroids[vectors_location[j]].remove(vectors[j])
        if vectors_location[j] != closest:
            centroids[closest].append(vectors[j])
        vectors_location[j] = closest
    for j in range(len(centroids_means)):
        new_mean = calculate_mean(centroids[j])
        if euclidean_distance(new_mean, centroids_means[j]) >= epsilon:
            below_epsilon = False
        centroids_means[j] = new_mean
    if below_epsilon:
        break
# printing method
for i in range(len(centroids_means)):
    for j in range(dimension):
        if j == dimension - 1:
            print(round(centroids_means[i][j], 4))
        else:
            print(round(centroids_means[i][j], 4), end=",")

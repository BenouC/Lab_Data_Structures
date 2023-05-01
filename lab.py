import sys

METHODS = ["single", "complete", "average", "ward"]

# Checks if the method passed in the arguments is supported
def isValidMethod(method):
    return method in METHODS

# Reads the data from the data file passed in the Arguments
def readFileData(filename):
    file_data = []
    with open(filename, 'r') as f:
        for line in f:
            data = line.split()
            for x in data:
                file_data.append(int(x))
    return file_data

# Method to either calculate the distance for points or whole clusters
# The else statement is not working yet
def calculateSingleDistance(cluster1, cluster2):
    #TODO Switch with other methods too    
    return calculateDistanceForPoints(cluster1, cluster2)

def hashify(cluster1, cluster2):
    # print(f"Distance of {cluster1} and {cluster2} is:")
    return f"{' '.join(map(str, cluster1))}, {' '.join(map(str, cluster2))}"

# 𝑑(𝑢, 𝑣) = 𝛼𝑖𝑑(𝑠, 𝑣) + 𝛼𝑗𝑑(𝑡, 𝑣) + 𝛽𝑑(𝑠, 𝑡) + 𝛾|𝑑(𝑠, 𝑣) − 𝑑(𝑡, 𝑣)|
# WIP
def calculateDistancesForClusters(clusters, s, t, distances):
    new_cluster = []
    new_cluster.extend(s)
    new_cluster.extend(t)

    for i, _ in enumerate(clusters):
        if i == len(clusters) - 1:
           continue

        # print(clusters[i])
        # print(distances[hashify(s, clusters[i])])
        # print(distances[hashify(t, clusters[i])])
        # print(abs(distances[hashify(s, clusters[i])] - distances[hashify(t, clusters[i])]))

        distance = 0.5 * ((distances[hashify(s, clusters[i])]) + distances[hashify(t, clusters[i])] - (abs(distances[hashify(s, clusters[i])] - distances[hashify(t, clusters[i])])))

        # print(clusters[i])
        # print(f"The distance of the {new_cluster} from {clusters[i]} is {distance}")

        distances[f"{' '.join(map(str, clusters[i]))}, {' '.join(map(str, new_cluster))}"] = distance
        distances[f"{' '.join(map(str, new_cluster))}, {' '.join(map(str, clusters[i]))}"] = distance


def calculateDistanceForPoints(cluster1, cluster2):
    min_dist = 99999999
    for i in cluster1:
        for j in cluster2:
            if abs(i - j) < min_dist:
                min_dist = abs(i - j)
    # print(f"Minimum Distamce for #{cluster1} and #{cluster2}: {min_dist}")
    return min_dist

def findInitialDistances(clusters, distances):
    # TODO: Extract this to a method and switch depending on the METHOD
    i = 0
    j = i + 1
    while i <= len(clusters) - 1:
        j = 0
        while j <= len(clusters) - 1:
            distance = calculateSingleDistance(clusters[i], clusters[j])
            distances[f"{' '.join(map(str, clusters[i]))}, {' '.join(map(str, clusters[j]))}"] = distance
            j += 1
        i += 1
    
# Search for similar clusters in order to group them
def findSimilarClusters(clusters, distances):
    i = 0
    j = i + 1
    min_i = -1
    min_j = -1
    min_distance = 999999
    while i <= len(clusters) - 1:
        j = 0
        while j <= len(clusters) - 1:
            if i != j:   
                distance = distances[f"{' '.join(map(str, clusters[i]))}, {' '.join(map(str, clusters[j]))}"]
                # print(f"Distance for {clusters[i]} and {clusters[j]} is {distance}")
                if distance < min_distance:
                    min_distance = distance
                    min_i = i
                    min_j = j
            j += 1
        i += 1
    
    return (min_i, min_j)

# The Big Clustering Loop
def cluster(data):
    # Put each number into its own cluster
    # It will look like this [[1], [2], [4], [8]], each subarray is a cluster
    distances = {}
    clusters = []
    new_clusters = []
    for item in data:
        clusters.append([item])

    
    findInitialDistances(clusters, distances)

    i = 0
    # While Clusters > 1
    while len(clusters) > 1:
        # Find the 2 most similar clusters
        print(f"Clustering loop: #{i}")
        result = findSimilarClusters(clusters, distances)

        # Remove the 2 old clusters
        new_clusters = [x for i,x in enumerate(clusters) if i != result[0] and i != result[1]]
        
        # Merge these 2 and add the a new one
        cluster1 = clusters[result[0]]
        cluster2 = clusters[result[1]]
        new_cluster = [*cluster1]
        new_cluster.extend(cluster2)
        new_clusters.append(new_cluster)
        print(new_clusters)
        clusters = new_clusters

        # Update Distances for new cluster
        calculateDistancesForClusters(clusters, cluster1, cluster2, distances)

        i += 1
        
# Main method where the code starts running
def main():
    method, input_filename = sys.argv[1], sys.argv[2]

    if not isValidMethod(method):
        raise ValueError("Invalid method passed as an argument")
    
    data = readFileData(input_filename)
    
    cluster(data)    


main()

#TODO: 
# - Switch to calculate the distances on a first loop
# - Traverse the distances and find the most similar one (Depending on the method)
# - Update the clusters and also calculate and update the distance of the new cluster to any other cluster
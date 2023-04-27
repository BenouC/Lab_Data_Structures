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
    

# 𝑑(𝑢, 𝑣) = 𝛼𝑖𝑑(𝑠, 𝑣) + 𝛼𝑗𝑑(𝑡, 𝑣) + 𝛽𝑑(𝑠, 𝑡) + 𝛾|𝑑(𝑠, 𝑣) − 𝑑(𝑡, 𝑣)|
# WIP
def calculateDistancesForClusters(clusters, s_index, t_index, distances):
    s = clusters[s_index]
    t = clusters[t_index]

    for i, cluster in enumerate(clusters):
        if i == t_index or i == s_index:
           continue
         
        distances = 0,5 * calculateDistanceForPoints(s, cluster) 
        + 0,5 * calculateDistanceForPoints(t, cluster)
        - 0,5 * abs(calculateDistanceForPoints(s, cluster) - calculateDistanceForPoints(t, cluster))
        

def calculateDistanceForPoints(cluster1, cluster2):
    min_dist = 99999999
    for i in cluster1:
        for j in cluster2:
            if abs(i - j) < min_dist:
                min_dist = abs(i - j)

    return min_dist

def findInitialDistances(clusters, distances):
    # TODO: Extract this to a method and switch depending on the METHOD
    i = 0
    j = i + 1
    min_i = -1
    min_j = -1
    min_distance = 999999
    while i <= len(clusters) - 1:
        j = i + 1
        while j <= len(clusters) - 1:
            distance = calculateSingleDistance(clusters[i], clusters[j])
            distances[i][j] = distance
            if distance < min_distance:
                min_distance = distance
                min_i = i
                min_j = j
            j += 1
        i += 1
    
    return (min_i, min_j)    

# Search for similar clusters in order to group them
def findSimilarClusters(clusters, distances):
    # TODO: Extract this to a method and switch depending on the METHOD
    i = 0
    j = i + 1
    min_i = -1
    min_j = -1
    min_distance = 999999
    while j <= len(clusters) - 1:
        distance = distances[i][j]
        if distance < min_distance:
            min_distance = distance
            min_i = i
            min_j = j
        i += 1
        j += 1

    return (min_i, min_j) 

# The Big Clustering Loop
def cluster(data):
    # Put each number into its own cluster
    # It will look like this [[1], [2], [4], [8]], each subarray is a cluster
    distances = [[0 for x in range(len(data))] for x in range(len(data))]
    clusters = []
    new_clusters = []
    for item in data:
        clusters.append([item])

    
    findInitialDistances(clusters, distances)

    # While Clusters > 1
    while len(clusters) > 1:
        # Find the 2 most similar clusters
        result = findSimilarClusters(clusters, distances)
        print(result)

        # Update Distances for new cluster
        # calculateDistancesForClusters(clusters, result[0], result[1])

        # Remove the 2 old clusters
        new_clusters = [x for i,x in enumerate(clusters) if i != result[0] and i != result[1]]
        
        # Merge these 2 and add the a new one
        new_cluster = [*clusters[result[0]]]
        new_cluster.append(*clusters[result[1]])
        new_clusters.append(new_cluster)
        print(new_clusters)
        clusters = new_clusters
        
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
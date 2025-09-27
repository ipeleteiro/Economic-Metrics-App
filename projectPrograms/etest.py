'''
SUBROUTINE optPlan(rulesGraph, start)
    FOR v <- 0 TO v <- LEN(rulesGraph)
        dist[v] <- INFINITY // initial distance from source to vertex v is set to infinite
    NEXT v
    previous[v] <- NULL // previous node in optimal path is unknown
    dist[start] <- 0  // distance of start to itself is 0

    nodesLeft <- rulesGraph //all nodes in the graph are first unoptimised
    WHILE nodesLeft > 0 DO
        maxD <- 0
        FOR i <- 0 TO LEN(dist)
            IF dist[i] > maxD
                maxD <- dist[i] // finds node with the greatest distance from start
            ENDIF
        NEXT i
        nodesLeft.DELETE(largestD)
        FOR neighbour <- 0 TO LEN(neighbours of largestD) // each neighbour of removed node
            altRoute <- maxD + dist_between(maxD, neighbour) // finds if alt route is < direct route
            IF altRoute > dist[neighbour]
                dist[neighbour] <- altRoute
                previous[neighbour] <- maxD
            ENDIF
        NEXT neighbour
    ENDWHILE
    RETURN previous // whole route
ENSUBROUTINE
'''


A = {'B': -10, 'C': 5}
B = {'C': 2, 'D': -1}
C = {'B': 2, 'D': -3}
D = {}

nodes = {'A': A, 'B': B, 'C': C, 'D': D}

start = 'A'
distance = {}

for node in nodes:
    if node == start:
        distance[node] = 0
    else:
        distance[node] = -100000


priorityQueue = ['A', 'B', 'C', 'D']
previous = []

while len(priorityQueue) > 0:
    currentNode = priorityQueue.pop(0)
    previous.append(currentNode)
    for neighbour in nodes[currentNode]:
        newDist = distance[currentNode] + nodes[currentNode][neighbour]
        if newDist > distance[neighbour]:
            distance[neighbour] = newDist
            sortedDist = dict(sorted(distance.items(), key=lambda item: item[1], reverse=True))
            temp = []
            for node in sortedDist:
                if node in priorityQueue:
                    temp.append(node)
            priorityQueue = temp

print(previous)
print(distance)
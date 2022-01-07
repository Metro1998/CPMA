# @author Metro
# @date 2022/1/7


import heapq
import os
import numpy as np


class Graph:

    def __init__(self, adjacent_matrix, threshold, save_path):
        self.vertices = adjacent_matrix
        self.size_matrix = adjacent_matrix.shape[0]
        self.threshold = threshold  # We set a threshold to control how long the shortest path will be.
        self.save_path = save_path  # Str.

    def neighbors(self, vertex):
        neighbors = [i for i, x in enumerate(self.vertices[vertex]) if x != 0]

        return neighbors

    def shortest_path(self, origin):
        distances = [0] * self.size_matrix  # Distance from origin to node, here we use vertex index as node
        previous = [None] * self.size_matrix  # Previous nodes in optimal path from origin
        nodes = []  # Priority queue of all nodes in Graph

        # Initialization
        for vertex in range(self.size_matrix):
            if vertex == origin:  # Set root node as distance of 0
                distances[vertex] = 0
                heapq.heappush(nodes, [0, vertex])  # TODO
            else:
                distances[vertex] = float('inf')  # Set distance to 2^32-1 in default
                heapq.heappush(nodes, [float('inf'), vertex])

        while nodes:
            smallest = heapq.heappop(nodes)[1]  # Vertex in nodes with smallest distance, and remove if from heapq
            if distances[smallest] == float('inf'):
                print('All remaining vertices are inaccessible from origin')
                break

            for neighbor in self.neighbors(smallest):  # Look at all the nodes that this vertex is attached to
                alt = distances[smallest] + self.vertices[smallest][neighbor]  # Alternative path distance
                if alt < distances[neighbor]:  # If there is a new shortest path, update our priority queue(relax)
                    if alt > self.threshold:
                        print('Break in advance.')
                        break
                    distances[neighbor] = alt
                    previous[neighbor] = smallest
                    for n in nodes:
                        if n[1] == neighbor:
                            n[0] = alt
                            break
                    heapq.heapify(nodes)
        return distances

    def __str__(self):
        return str(self.vertices)

    def update_shortest_path_matrix(self):
        shortest_path_matrix = []
        for vertex in range(self.size_matrix):
            distance = self.shortest_path(vertex)
            shortest_path_matrix.append(distance)
        shortest_path_matrix = np.array(shortest_path_matrix)
        # if os.path.exists('../data/shortest_path_matrix.npy'):
        #     os.remove('../data/shortest_path_matrix.npy')
        #     print('Delete successfully.')

        return shortest_path_matrix


if __name__ == '__main__':
    adj_matrix = np.array([[0, 2, 4, 2, 0], [2, 0, 1, 0, 3], [4, 1, 0, 5, 2],
                           [2, 0, 5, 0, 2], [0, 3, 2, 2, 0]])
    g = Graph(adjacent_matrix=adj_matrix, threshold=100, save_path=None)
    print(g.update_shortest_path_matrix())
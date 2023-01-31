from itertools import permutations, combinations
from graph_task import Graph
import time

def pruneGraphs(size):
    vertices = []
    for i in range(size):
        vertices += [i + 1]
    allEdges = list(permutations(vertices, 2))
    for cntEdges in range(size * (size - 1) + 1):
        edgeCombos = combinations(allEdges, cntEdges)
        for edges in edgeCombos:
            g = Graph(vertices, edges)
            violates = g.violates()
            subViolates = g.subViolates()
            if violates != subViolates:
                g.showGraph()
                return
    print('violations and subviolatons are equivalent for ' + str(size) + '-diamond tasks.')

g = Graph([1,2,3], [(1,2),(2,1)])
g.showGraph()

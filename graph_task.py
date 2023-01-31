from itertools import combinations
from graphviz import Digraph
import tempfile
import os

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz/bin'


class Graph():
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.size = len(self.vertices)
        self.edges = edges
        self.priorsDict = {}
        for vertex in vertices:
            priors = []
            for edge in edges:
                if edge[1] == vertex:
                    priors += [edge[0]]
            self.priorsDict[vertex] = priors

    def infoMatrix(self):
        infos = {}
        for pair in combinations(self.vertices, 2):
            info = {}
            for vertex in self.vertices:
                info[vertex] = None
            for vertex in pair:
                for prior in self.priorsDict[vertex]:
                    info[prior] = 0
            for vertex in pair:
                info[vertex] = 1
            infos[pair] = info
        return infos

    def violates(self):
        infos = self.infoMatrix()
        for twoPair in combinations(list(combinations(self.vertices, 2)), 2):
            twoPairViolates = True
            pairi = twoPair[0]
            pairj = twoPair[1]
            infoi = infos[pairi]
            infoj = infos[pairj]
            for v in self.vertices:
                if (infoi[v] == 0 and infoj[v] == 1) or (infoj[v] == 0 and infoi[v] == 1):
                    twoPairViolates = False
                    break
            if twoPairViolates and ((pairi[0] in pairj) or (pairi[1] in pairj)):
                return True
        return False

    def subViolates(self):
        for subVertices in combinations(self.vertices, 3):
            subEdges = []
            for edge in self.edges:
                if (edge[0] in subVertices) and (edge[1] in subVertices):
                    subEdges += [edge]
            subGraph = Graph(subVertices, subEdges)
            if subGraph.violates():
                return True
        return False

    def showGraph(self):
        g = Digraph(
            format='jpg',
            name='Graph',
            graph_attr={'regular': 'true', 'layout':'circo'},
            node_attr={'shape': 'circle', 'fixedsize': 'shape', 'width':'0.35', 'height':'0.35'},
            edge_attr={})
        for vertex in self.vertices:
            g.node(str(vertex))
        for edge in self.edges:
            g.edge(str(edge[0]), str(edge[1]))
        g.view(tempfile.mktemp(''))

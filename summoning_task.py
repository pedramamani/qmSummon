from numpy import linalg as la
from graphviz import Digraph
import tempfile
import os

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz/bin'


#Represent a summoning task as a directed graph
class SummoningTask:
    def __init__(self, rels):
        self.diamonds = list()
        self.connections = list()
        self.violates = None
        self.violation = {}
        self.entanglements = {}
        self.countDiamonds = 0
        for rel in rels:
            if isinstance(rel, tuple):
                preDiam, postDiam = Diamond(rel[0]), Diamond(rel[1])
                addPre, addPost = True, True
                for diamond in self.diamonds:
                    if diamond == preDiam:
                        preDiam = diamond
                        addPre = False
                    if diamond == postDiam:
                        postDiam = diamond
                        addPost = False
                if addPre:
                    self.diamonds += [preDiam]
                    self.countDiamonds += 1
                if addPost:
                    self.diamonds += [postDiam]
                    self.countDiamonds += 1
                preDiam.addPost(postDiam)
                postDiam.addPre(preDiam)
                self.connections += [(preDiam, postDiam)]
            else:
                diam = Diamond(rel)
                self.diamonds += [diam]
                self.countDiamonds += 1
        self.diamonds.sort(key = lambda d: d.getLabel())
        self.connections.sort(key = lambda pair: pair[0].getLabel())

    def getDiamonds(self):
        return self.diamonds

    def getCountDiamonds(self):
        return self.countDiamonds

    def violatesMonogomy(self):
        if self.violates is None:
            self.__entangle()
            for (di1, di2), infoi in self.entanglements.items():
                for (dj1, dj2), infoj in self.entanglements.items():
                    compare = True
                    if (di1 == dj1 and not di2 == dj2):
                        d, di, dj = di1, di2, dj2
                    elif (di1 == dj2 and not di2 == dj1):
                        d, di, dj = di1, di2, dj1
                    elif (di2 == dj1 and not di1 == dj2):
                        d, di, dj = di2, di1, dj2
                    elif (di2 == dj2 and not di1 == dj1):
                        d, di, dj = di2, di1, dj1
                    else:
                        compare = False
                    if compare:
                        if self.__agree(infoi, infoj):
                            self.violation[d] = (di, dj)
        self.violates = bool(self.violation)
        return self.violates

    def __agree(self, l1, l2):
        for e1, e2 in zip(l1, l2):
            if e1 is not None and e2 is not None:
                if not e1 == e2:
                    return False
        return True

    def __entangle(self):
        for i in range(self.countDiamonds):
                for j in range(i + 1, self.countDiamonds):
                    di = self.diamonds[i]
                    dj = self.diamonds[j]
                    di.setCall(True)
                    dj.setCall(True)
                    listij = []
                    for d in self.diamonds:
                        if (d in di.getPre() or d == di) or (d in dj.getPre() or d == dj):
                            listij += [d.getCall()]
                        else:
                            listij += [None]
                    self.entanglements[(di, dj)] = listij
                    di.setCall(False)
                    dj.setCall(False)

    def printTask(self):
        if bool(self.diamonds):
            print("Diamonds: ", end = "")
            for diam in self.diamonds:
                print(diam.getLabel(), end = " ")
            if bool(self.connections):
                print("\nConnections: ", end = "")
                for connection in self.connections:
                    pre, post = connection
                    print("\n" + pre.getLabel() + " -> " + post.getLabel(), end = "")
            print()

    def printCausalMatrix(self):
        if bool(self.diamonds):
            print("Causal Matrix: \n", end = "")
            mat = []
            row = []
            for d1 in self.diamonds:
                for d2 in self.diamonds:
                    if d1 == d2 or (d1, d2) in self.connections:
                        row += [1]
                    else:
                        row += [0]
                mat += [row]
                row = []
            eigvals, eigvects = la.eig(mat)
            for row in mat:
                for val in row:
                    print(str(val) + " ", end = "")
                print()
            print("Eigenvalues: \n", end = "")
            for eigval in eigvals:
                print("%.2f"%eigval + " ", end = "")
            print("\nEigenvectors: \n", end = "")
            for eigvect in eigvects:
                for val in eigvect:
                    print("%.2f"%val + " ", end = "")
                print()

    def printViolation(self):
        if self.violates is None:
            self.violatesMonogomy()
        if self.violates:
            for d, (di, dj) in self.violation.items():
                print(d.getLabel() + " violates monogomy by entanglement with " +
                      di.getLabel() + " and " + dj.getLabel() + ".")
        else:
            print("Does not violate monogomy.")

    def printEntanglements(self):
        if not bool(self.entanglements):
            self.__entangle()
        if bool(self.entanglements):
            print("Entanglements: ")
            for (d1, d2), info in self.entanglements.items():
                print(d1.getLabel() + "," + d2.getLabel() + ": ", end = "")
                for call in info:
                    if call is None:
                        print("x ", end = "")
                    elif call:
                        print("1 ", end = "")
                    else:
                        print("0 ", end = "")
                print()

    def showGraph(self):
        print('Outputting graph...')
        
        g = Digraph(
            format='jpg',
            name='Graph',
            graph_attr={'regular': 'true', 'layout':'circo'},
            node_attr={'shape': 'circle', 'fixedsize': 'shape', 'width':'0.35', 'height':'0.35'},
            edge_attr={}
        )

        for diamond in self.diamonds:
            g.node(diamond.getLabel())
        for connection in self.connections:
            g.edge(connection[0].getLabel(), connection[1].getLabel())
        g.view(tempfile.mktemp(''))


#Represent a diamond as a vertex
class Diamond:
    def __init__(self, label):
        self.label = str(label)
        self.preSet = list()
        self.postSet = list()
        self.call = False

    def __eq__(self, other):
        return self.label == other.label

    def __hash__(self):
        if len(self.label) == 0:
            return 0
        else:
            return int(self.label[0])

    def addPre(self, pre):
        if isinstance(pre, Diamond):
            self.preSet += [pre]

    def addPost(self, post):
        if isinstance(post, Diamond):
            self.postSet += [post]

    def connectsTo(self, other):
        return other in postSet

    def isConnectedToBy(self, other):
        return other in preSet

    def getPre(self):
        return self.preSet

    def getPost(self):
        return self.postSet

    def getLabel(self):
        return self.label

    def getCall(self):
        return self.call

    def setCall(self, call):
        self.call = bool(call)

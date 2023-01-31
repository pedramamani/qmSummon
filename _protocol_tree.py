# A class for storing protocol trees and visualizing them

class ProtocolTree:
    def __init__(this, label):
        this.label = label
        this.topCondition = None
        this.bottomCondition = None
        this.topState = None
        this.bottomState = None

    def __eq__(this, that):
        return isinstance(that, ProtocolTree) and this.label == that.label

    def setTop(this, condition, state):
        this.topCondition = condition
        this.topState = state

    def setBottom(this, condition, state):
        this.bottomCondition = condition
        this.bottomState = state

    def printTree(this):
        print("Protocol Tree:")
        for line in this.__getTreePrint():
            print(line)

    def __getTreePrint(this):
        treePrint = [" " + this.label + " "]
        if this.topState is not None:
            subPrint = this.topState.__getTreePrint()
            treePrint[0] += "--" + this.topCondition + "-->" + subPrint[0]
            if len(subPrint) > 1:
                for line in subPrint[1:]:
                    treePrint.append(" " * (len(this.label) + 1) + "|" + " " * (len(this.topCondition) + 5) + line)
        if this.bottomState is not None:
            subPrint = this.bottomState.__getTreePrint()
            if this.topState is not None:
                treePrint.append(" " * (len(this.label) + 1) + "|--" + this.bottomCondition + "-->" + subPrint[0])
            else:
                treePrint[0] += "--" + this.bottomCondition + "-->" + subPrint[0]
            if len(subPrint) > 1:
                for line in subPrint[1:]:
                    treePrint.append(" " * (len(this.topCondition) + len(this.label) + 7) + line)
        return treePrint

    def getLabel(this):
        return this.label

    def getTopCondition(this):
        return this.topCondition

    def getBottomCondition(this):
        return this.bottomCondition

    def getTopState(this):
        return this.topState

    def getBottomState(this):
        return this.bottomState

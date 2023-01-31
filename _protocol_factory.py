from _protocol_tree import ProtocolTree
from summoning_task import SummoningTask

protocol = SummoningTask({(1,2),(3,2),(3,4),(1,4),(4,2)})
protocol.printTask()
protocol.printEntanglements()
protocol.printViolation()

p24 = ProtocolTree("24")
p23 = ProtocolTree("23")
p12 = ProtocolTree("12")
p34 = ProtocolTree("34")
p14 = ProtocolTree("14")
p13 = ProtocolTree("13")
p13.setTop("b1=0", p34)
p13.setBottom("b3=0", p14)
p34.setTop("b3=0", p24)
p34.setBottom("b4=0", p23)
p14.setTop("b1=0", p24)
p14.setBottom("b4=0", p12)
p13.printTree()

input("Press Enter to exit...")

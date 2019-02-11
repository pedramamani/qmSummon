from protocol import Protocol, Diamond

while(True):
    p = input("Enter a protocol by specifying its causal connections: ")
    protocol = Protocol(eval("{" + p + "}"))
    protocol.printProtocol()
    protocol.printCausalMatrix()
    protocol.printEntanglements()
    protocol.printViolation()
    print()

from summoning_task import *


while True:
    inText = eval('[' + input('Input graph. Example (1,2),(3): ') + ']')
    if inText == []:
        break
    
    task = SummoningTask(inText)
    task.printViolation()
    task.showGraph()
    print()

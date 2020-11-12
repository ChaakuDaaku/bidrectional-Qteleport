import sys
from cqc.pythonLib import qubit, CQCConnection, CQCMix

def aliceNode():

    shots = int(sys.argv[1])
    states = { "ASent": [], "ARecv": [] }

    for i in range(shots):

        with CQCConnection("Alice") as Alice:

            #Creating EPR and Alice's qubit
            qA = Alice.createEPR("Bob")
            q = qubit(Alice)

            #Teleportation operation
            q.H()
            q.cnot(qA)
            q.H()

            a = q.measure()
            b = qA.measure() #I don't want to destroy the qubit after measurement

            states["ASent"].append(a)
            Alice.sendClassical("Bob", [a, b])

            qA = Alice.recvEPR()
            data = Alice.recvClassical()
            message = list(data)

            c = message[0]
            d = message[1]

            if d == 1:
                qA.X()
            if c == 1:
                qA.Z()
        
            m = qA.measure()

            states["ARecv"].append(m)

    print("A's Node:", states)


if __name__ == "__main__":
    aliceNode()

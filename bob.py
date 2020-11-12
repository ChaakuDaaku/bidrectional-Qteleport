import sys
from cqc.pythonLib import qubit, CQCConnection

def bobNode():
    
    shots = int(sys.argv[1])
    states = { "BRecv": [], "BSent": [] }

    for i in range(shots):

        with CQCConnection("Bob") as Bob:

            #Receving Alice's EPR
            qB = Bob.recvEPR()

            data = Bob.recvClassical()
            message = list(data)

            a = message[0]
            b = message[1]

            if b == 1:
                qB.X()
            if a == 1:
                qB.Z()

            m = qB.measure()
            states["BRecv"].append(m)

            #Just flipping the previous outcome for fun
            n = 2**m - 1

            #Creating Bob's own qubit and EPR
            qB = Bob.createEPR("Alice")
            q = qubit(Bob)

            #Using the flipped outcome
            if n:
                q.X()

            q.H()
            q.cnot(qB)
            q.H()

            c = q.measure()
            d = qB.measure()
            
            states["BSent"].append(c)
            Bob.sendClassical("Alice", [c, d])  

    print("B's Node:", states)


if __name__ == "__main__":
    bobNode()

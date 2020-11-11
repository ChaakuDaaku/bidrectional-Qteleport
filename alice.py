from cqc.pythonLib import qubit, CQCConnection

def aliceNode():

    with CQCConnection("Alice") as Alice:

        print("||   First Alice sends a message to Bob  ||")
        print("-"*25)

        #Creating EPR and Alice's qubit
        qA = Alice.createEPR("Bob")
        q = qubit(Alice)

        #Teleportation operation
        q.H()
        q.cnot(qA)
        q.H()

        a = q.measure()
        b = qA.measure(inplace=True) #I don't want to destroy the qubit after measurement

        print("Alice: Measurement outcomes of A->B are: a={}, b={} \n\n".format(a, b))

        Alice.sendClassical("Bob", [a, b])

        #TODO: Can we avoid the next line? Maybe.
        # But I am getting inconsisten results if I do not re-initialise qA.
        # If I do this, line 19's 'inplace' arg becomes technically useless.
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
        print("Alice: Measurement outcomes of B->A is: {}".format(m))
        print("-"*50)


if __name__ == "__main__":
    aliceNode()
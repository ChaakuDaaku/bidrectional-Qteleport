from cqc.pythonLib import qubit, CQCConnection

def bobNode():

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

        m = qB.measure(inplace=True) #Similar to Alice's retention of qA.
        print("Bob: Measurement outcomes of A->B is: {}".format(m))
        print("-"*50+"\n\n")

        #Just flipping the previous outcome for fun
        n = 2**m - 1

        print("||   Now, Bob will send a message to Alice   ||")
        print("-"*25)

        #Creating Bob's own qubit and
        # controversially recreating EPR (Refer line 25 in Alice's code)
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

        print("Bob: Measurement outcomes of B->A are: c={}, d={} \n\n".format(c, d))

        Bob.sendClassical("Alice", [c, d])


if __name__ == "__main__":
    bobNode()
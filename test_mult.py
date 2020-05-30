# load library
from Library.Spout import Spout

import random

def main() :
    # create spout object
    spout = Spout(silent = True, n_rec = 3, n_send = 3)
    # create receiver
    spout.createReceiver('input1', id = 0)
    spout.createReceiver('input2', id = 1)
    spout.createReceiver('input3', id = 2)
    # create sender
    spout.createSender('output1', id = 0)
    spout.createSender('output2', id = 1)
    spout.createSender('output3', id = 2)

    while True :

        # check on close window
        spout.check()
        # receive data
        data = spout.receive(id = 0)
        data1 = spout.receive(id = 1)
        data2 = spout.receive(id = 2)
        # send data
        if random.random()  > .9:
            spout.send(data1)
            spout.send(data, 1)
        else:
            spout.send(data)
            spout.send(data1, 1)
        
        spout.send(data2, id = 2)

    
if __name__ == "__main__":
    main()
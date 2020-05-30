# load library
from Library.Spout import Spout

import random

def main() :
    # create spout object
    spout = Spout(silent = False)
    # create receiver
    spout.createReceiver('input1')
    # create sender
    spout.createSender('output1')

    while True :

        # check on close window
        spout.check()
        # receive data
        data = spout.receive()

        # send data
        spout.send(data)

    
if __name__ == "__main__":
    main()
from Library.Spout import Spout

def main() :
    spout = Spout(silent = True)
    spout.createReceiver('input')
    spout.createSender('output')

    while True :

        spout.check()
        data = spout.receive()
        spout.send(data)
    
if __name__ == "__main__":
    main()
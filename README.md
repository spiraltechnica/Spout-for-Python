# Spout for Python

Based on https://github.com/spiraltechnica/Spout-for-Python

A modified Spout library using Boost::Python to enable Spout texture sharing using Python.
This library is for use with Python 3.5 / 3.6 / 3.7 64bit. Now it will automatically define python version and load appropriate file.

## Using the Library
```python test.py```
or just check sample code in the test.py
```
# import library
from Library.Spout import Spout

def main() :
    # create spout object
    spout = Spout(silent = True)
    # create receiver
    spout.createReceiver('input')
    # create sender
    spout.createSender('output')

    while True :
        # check on exit
        spout.check()
        # receive data
        data = spout.receive()
        # send data
        spout.send(data)
    
if __name__ == "__main__":
    main()
```

## Parameters 
Parameters and arguments for sender and receiver can be checked in the ```Library/Spout.py```

## Requirements

```
pip install -r requirements.txt
```

- pygame
- pyopengl

## Additional
* Support multiple spount instances (if you want have multiple sender/receivers)
* Now it can be used as any python library, just few lines of code
* Automatically define the size of receiver and data to send

# Add relative directory ../Library to import path, so we can import the SpoutSDK.pyd library. Feel free to remove these if you put the SpoutSDK.pyd file in the same directory as the python scripts.
import sys
sys.path.append('../Library')

import SpoutSDK

x = SpoutSDK.SpoutSender()

print(x.SayHello())




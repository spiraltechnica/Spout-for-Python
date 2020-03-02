# Spout for Python

![TD](Images/spout.JPG?raw=true)

Based on https://github.com/spiraltechnica/Spout-for-Python

A modified Spout library using Boost::Python to enable Spout texture sharing using Python.

This library is for use with Python 3.5 / 3.6 / 3.7 64bit. 

It was built against Boost 1.72 and Python 3.7-amd64 using Visual Studio 2019 on Windows 10 64bit

This modified library does not yet fully implement the functionality available in the SpoutSDK. 

## Using the Library
The SpoutSDK.pyd library is located in the [Library/](Library/) folder of this repository. Choose desired python version and ename it to 'SpoutSDK.pyf'

You shouldn't need to compile Boost or have Visual Studio installed to run these examples and integrate the library into your own Python projects

## Template

Use ```template.py``` to run a test:

```python template.py``` will run with all default values
```python template.py --type output --spout_size 1280 720 --spout_output_name out``` output 1280x720 textue with name 'out'

## Data processing
use ```main_pipeline``` function to do our data processing. It has input texture from receiver if active or white if receiver not active, and should return texture for sender if output desired.

```""" here your functions """
def main_pipeline(data):
    output = data
    return output
```


## Arguments
--type input/output/input-output
--spout_size Width and height of the spout receiver and sender
--spout_input_name Spout receiving name
--spout_output_name Spout sending name
--silent True if want hide pyGame window


You'll need
- pygame
- pyopengl

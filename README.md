# Spout for Python
A modified Spout library using Boost::Python to enable Spout texture sharing using Python.
![Spout for Python](https://raw.githubusercontent.com/spiraltechnica/Spout-for-Python/master/Images/neural%20style%20resolume.png)
This library is for use with Python 3.5 64bit. 

It was built against Boost 1.65 and Python 3.5.2-amd64 using Visual Studio 2015 on Windows 10 64bit

The Visual Studio solution depends on:

- Boost being located in C:\Program Files\boost_1_65_0 and

- Python 3.5 64bit being located in %UserProfile%\AppData\Local\Programs\Python\Python35\include 

This modified library does not yet fully implement the functionality available in the SpoutSDK. 

## Using the Library
The SpoutSDK.pyd library is located in the [Library/](Library/) folder of this repository. The example files are in the [Examples/](Examples/) folder. 

You shouldn't need to compile Boost or have Visual Studio installed to run these examples and integrate the library into your own Python projects

And of course, if you don't have Spout installed, you'll definitely need to get it and install it. It's available at http://spout.zeal.co/

## Examples


Take a look in the [Examples/](Examples/) folder for a list of python scripts that can interface with the modified SpoutSDK.pyd library.

The simplest example file is ```hello.py```. This merely attempts to import the library, create an instance of a Spout Sender, and call a function that returns text into the console. 

The example scripts ```spout_NST_receiver.py``` and ```spout_NST_sender_receiver.py``` will not run by themselves, because they are designed to work with Tensorflow Fast Style Transfer, located at https://github.com/hwalsuklee/tensorflow-fast-style-transfer

### Running the Examples

A number of the examples will require libraries not in the base Python 3.5 install. That base install is available at https://www.python.org/downloads/release/python-352/

You'll need
- numpy-1.13.1+mkl-cp35-cp35m-win_amd64.whl
- opencv_python-3.3.0-cp35-cp35m-win_amd64.whl
- pygame-1.9.3-cp35-cp35m-win_amd64.whl

From the Unofficial Windows Binaries for Python Extension Packages at http://www.lfd.uci.edu/~gohlke/pythonlibs/ 

Install them using the pip3 manager that comes with Python 3.5, using the ```pip install <filename>``` command from the command line.

In addition to the aforementioned packages, you'll need PyOpenGL from the pip default repositories:
- Install using ```pip install PyOpenGL``` command. The version I'm using is PyOpenGL 3.1.0
- It would be also worth installing Pillow with ```pip install Pillow```. I'm using Pillow 4.2.1

## Building Boost
- Download the Boost 1.65 source for windows from http://www.boost.org/users/history/version_1_65_0.html
- Extract to C:\Program Files\boost_1_65_0
- Open an Administrative access Command Prompt (right click on Command Prompt and Run As Administrator)
- cd into C:\Program Files\boost_1_65_0
- Type ```boostrap.bat``` and run the command
- Now run ```.\b2.exe --stagedir=./stage/x64 address-model=64 --build-type=complete --toolset=msvc-14.0 --threading=multi --runtime-link=shared --variant=debug```

This will take some time. Once it's complete run 
- ```.\b2.exe --stagedir=./stage/x64 address-model=64 --build-type=complete --toolset=msvc-14.0 --threading=multi --runtime-link=shared --variant=release```

Which will also take some time. However, it should say it is successfully built at the end and give you locations for linker library include paths and compiler include paths.

## Building the DLL

With Boost and Python installed you should now be able to use Visual Studio 2015 and build the ```SpoutSDK.dll``` for 64bit architecture in Debug and Release modes. In order to interface the dll with Python, rename the dll from ```SpoutSDK.dll``` to ```SpoutSDK.pyd```.

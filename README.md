# Spout for Python
A modified Spout library using Boost::Python to enable Spout texture sharing using Python.

![Spout for Python](https://raw.githubusercontent.com/spiraltechnica/Spout-for-Python/master/Images/neural%20style%20resolume.png)

This library is for use with Python 3.7 64bit.

It was built against Boost 1.69 and Python 3.7.2-amd64 using Visual Studio 2017 on Windows 10 64bit

This modified library does not yet fully implement the functionality available in the SpoutSDK.

## Using the Library
The SpoutSDK.pyd library is located in the [Library/](Library/) folder of this repository. The example files are in the [Examples/](Examples/) folder.

You shouldn't need to compile Boost or have Visual Studio installed to run these examples and integrate the library into your own Python projects, but you'll definitely need to install [Spout](http://spout.zeal.co/).

## Examples


Take a look in the [Examples/](Examples/) folder for a list of python scripts that can interface with the modified SpoutSDK.pyd library.

The simplest example file is ```hello.py```. This merely attempts to import the library, create an instance of a Spout Sender, and call a function that returns text into the console.

The example scripts ```spout_NST_receiver.py``` and ```spout_NST_sender_receiver.py``` will not run by themselves, because they are designed to work with Tensorflow Fast Style Transfer, located at https://github.com/hwalsuklee/tensorflow-fast-style-transfer

### Running the Examples

A number of the examples will require libraries not in the base Python 3.7 install. That base install is available at https://www.python.org/ftp/python/3.7.2/python-3.7.2-amd64.exe

You'll need

- numpy         1.16.2
- opencv-python 4.0.0.21
- pygame        1.9.4
- PyOpenGL      3.1.0

Install them using the pip manager that comes with Python 3.7, using the ```pip install <filename>``` command from the command line.

- It would be also worth installing Pillow with ```pip install Pillow```. I'm using Pillow 4.2.1

## Building Boost
Requires the prior installation of [MS Visual Studio 17](https://visualstudio.microsoft.com/de/vs/) Community Edition.

- Download the Boost 1.69 source for windows from https://www.boost.org/users/history/version_1_69_0.html
- Extract to C:\Program Files\boost_1_69_0
- Open an Administrative access Command Prompt (right click on Command Prompt and Run As Administrator)
- cd into C:\Program Files\boost_1_69_0
- Type ```boostrap.bat``` and run the command

- Now run ```.\b2.exe --stagedir=./stage/x64 address-model=64 --build-type=complete --toolset=msvc-14.1 --threading=multi --runtime-link=shared --variant=debug```

This will take some time creating the debug libraries. Once it's complete run
- ```.\b2.exe --stagedir=./stage/x64 address-model=64 --build-type=complete --toolset=msvc-14.1 --threading=multi --runtime-link=shared --variant=release```

Which most likely will take much less time to create the release libraries. However, it should say it is successfully built at the end and give you locations for linker library include paths and compiler include paths. You only need them if you decided to extract and build boost at a different location.

## Building the DLL rsp. PYD

The Visual Studio solution depends on:

- Boost being located in C:\Program Files\boost_1_69_0 and

- Python 3.7 64bit being located in %UserProfile%\AppData\Local\Programs\Python\Python37\include

With Boost and Python installed you should now be able to use Visual Studio 2017 and build the ```SpoutSDK.dll``` for 64bit architecture in Debug and Release modes. In order to interface the dll with Python, rename the dll from ```SpoutSDK.dll``` to ```SpoutSDK.pyd```.

## Credits

- Ryan Walker (http://www.spiraltechnica.com/)
- Martin Froehlich (http://tecartlab.com)

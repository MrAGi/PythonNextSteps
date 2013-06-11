#Installing additional tools

##Introduction
This section will provide explanations of how to install the various additional tools required for this series of tasks.

##PyQt4
Installing PyQt4 is pretty straight-forward. Please follow the appropriate instructions for your platform:

- [Install PyQt4 on Mac OS X][59] (Please use MacPorts method)
- [Install PyQt4 on Windows][60]

##Matplotlib
Matplotlib is plotting library that will enable us to visualise graphs and charts.

###Install on Mac OS X
Please ensure that you have installed Python and PyQt4 via the MacPorts method before attempting to install Matplotlib.

1. Open the terminal application
2. Type **`sudo port py33-matplotlib`** - you will be prompted for your password.
3. Matplotlib should be installed

###Install on Windows
To install on Windows ensure that you know whether your Windows machine is 32-bit or 64-bit and then download the **latest stable version** of Matplotlib for Python 3.3 from the [Matplotlib downloads page][61].

##Numpy
Numpy provides a library that is necessary to run Matplotlib. If you have installed Matplotlib using the above method then you have already installed Numpy.

##Network X
Network X is a library that enables us to quickly create and use graphs.

###Install on Mac OS X
These instructions assume that you have used MacPorts for the above installations.

1. Download the [source for network x][62] (currently networkx-1.7.zip) 
2. Unzip this
3. Open the terminal application
4. type **`cd /Users/username/Downloads/networkx-1.7`**
    - ensure that you change **username** to your user name
    - this assumes that you downloaded and unzipped the file into the downloads folder
5. type **`python3.3 setup.py build`**
6. type **`sudo python3.3 setup.py install`** - you will be prompted for your password
7. Network X should be installed

###Install on Windows
These instructions assume that you have [Python on your path][63].

1. Download the [source for network x][62] (currently networkx-1.7.zip) 
2. Unzip this to your desktop
3. Open the command prompt
4. type **`cd Desktop`**
5. type **`cd networkx-1.7`**
5. type **`python setup.py build`**
6. type **`python setup.py install`**
7. Network X should be installed

##cx_Freeze
cx_Freeze is a set of utilities designed to produce versions of your applications that can be distributed without the having to install Python first.

Please follow the instructions for your platform:

- [Install on Mac OS X][63]
- [Install on Windows][64]

##Python Twitter
Python twitter is a library that enables you to connect to the Twitter API via Python. In addition to installing the software you will also need a [twitter developer account][65] and have created an application from within your twitter developer account (see [Creating a twitter application]).

###Install on Mac OS X
These instructions assume that you have used MacPorts for the above installations.

1. Download the [source python twitter][66] as a zip file
2. Unzip this
3. Open the terminal application
4. type **`cd /Users/username/Downloads/twitter-master`**
    - ensure that you change **username** to your user name
    - this assumes that you downloaded and unzipped the file into the downloads folder
5. type **`python3.3 setup.py build`**
6. type **`sudo python3.3 setup.py install`** - you will be prompted for your password
7. Python Twitter should be installed

###Install on Windows
These instructions assume that you have [Python on your path][63].

1. Download the [source python twitter][66] as a zip file
2. Unzip this to the desktop
3. Open the command prompt
4. type **`cd Desktop`**
5. type **`cd twitter-master`**
5. type **`python setup.py build`**
6. type **`python setup.py install`** - you will be prompted for your password
7. Python Twitter should be installed

##Creating a twitter application
In order to use Twitter from within Python you must have created an application from with the [Twitter developer][65] portal.

1. Make sure you are signed into the [Twitter developer][65] portal
2. Select 'My applications' from the menu 
3. Click on the button that says 'Create new application' 
4. Fill in the form 
5. From your list of applications make a note of the consumer key, consumer secret and the application name 

![][67]

[59]: http://www.pythonschool.net/mac_pyqt/
[60]: http://www.pythonschool.net/pyqt_windows/
[61]: http://matplotlib.org/downloads.html
[62]: https://pypi.python.org/pypi/networkx/
[63]: http://www.pythonschool.net/cxfreeze_win/
[64]: http://www.pythonschool.net/cxfreeze_mac/
[65]: https://dev.twitter.com
[66]: https://github.com/sixohsix/twitter
[67]: images/twitter_step4.png

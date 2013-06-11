#New Adventures in Python

##Introduction

Everyone is learning Python, or so it seems. 

There has been an explosion of interest in learning to program over the past couple of years and Python is right on the front line...and so it should be. It is an excellent programming language; it is easy to pick up and you can quickly learn enough to teach to GCSE level and even AS level. However, this statement crops up all to often:

"Python is great but it can't do **x**..."

Whatever *x* is Python can do it. Python provides enough flexibility to teach anything and everything that is required by both the AQA and OCR A-Level syllabuses (and beyond). This session will give you a flavour of what is possible, provide you with some examples (including code) and some jumping off points for further investigation.

##Assumptions

This session isn't for everybody...it makes some assumptions about your prior knowledge and experience. To get the most out of this session it is expected that you are already a Python programmer or are at least confident with the following in another language:

- Variables
- Selection
- Iteration
- Lists
- Functions
- File handling

It also assumes that you have some familiarity with either the AQA or OCR A-Level Computing specifications. Whilst I will highlight specification points at times, I will not necessarily explain them in depth (or at all).

Finally, all of the examples and code are in Python 3. 

##Requirements

All of the examples presented in this session require some additional tools to be installed over and above the basic requirement of Python 3. 

All of the examples were written and tested with Python 3.3.2, which was the most recent version available as of 27th May 2013.

In addition to Python 3 you will be required to install:

- [PyQt4][7]
- [Matplotlib][8]
- [Numpy][9]
- [Network X][10]
- [cx_Freeze][11]
- [Python Twitter][12]

You will also need accounts with the following services for some of the examples:

- [Twitter][20]
- [Open Exchange Rates][21]

If you don't want to install of this just now that's fine. Each example will highlight its own specific requirements.

Finally, it should be noted that the examples were written and tested on a Mac running OS X 10.8.3 but most were also tested under Windows 7.

##Time to make a start

Each of the examples have been designed to highlight different aspects of the Computing syllabus and show how Python can be used to teach them in a practical way. 

|[**Field Simulation**][18]||
----|------|
![][1]|The field simulation can be used to introduce **object-oriented programming** and **event-driven programming**. By creating a very basic simulation of a field (complete with crops and animals) students will get a taste of what it is like to develop a large(r) scale system.|
|[**Coffee Shop**][13]||
![][2]|The coffee shop example provides a good introduction to **databases** but here the focus is on accessing the data through a graphical user interface and presenting reports as **graphs**.|
|[**Google Maps**][14]||
![][3]|Find out the GPS co-ordinates of any address that the user enters. This is a nice introduction to **networking**, **client-server** and the **tcp/ip protocol stack**.|
|[**Currency Converter**][15]||
![][4]|A classic exercise that all students will attempt at some point - taking x amount of one currency and convert it into another. Let's make sure it is accurate though by collecting actual data from the Internet! Provides a nice way to introduce *networking*, **client-server** and *graphs*.|
|[**London Underground**][16]||
![][5]|Create a representation of the London Underground as a **graph** and then use that **graph** to provide directions between stations.|
|[**Twitter followers**][17]||
![][6]|Find out who is following who by downloading your follower information from Twitter and constructing a **graph** from them.|
|[**Distributing applications**][19]|
||Give your applications away by discovering how to create distributable versions of your Python code.|

[1]: images/field.png "Field Simulation"
[2]: images/coffee_shop.png "Coffee Shop Reports"
[3]: images/google_maps.png "Google Maps GPS"
[4]: images/currency_converter.png "Currency Converter"
[5]: images/tube_map.png "Underground Map"
[6]: images/twitter_followers.png "Twitter followers"
[7]: installing.md#pyqt4
[8]: installing.md#matplotlib
[9]: installing.md#numpy
[10]: installing.md#network-x
[11]: installing.md#cx_freeze
[12]: installing.md#python-twitter
[13]: Coffee%20Shop%20Graphs/README.md
[15]: Currency%20Converter/README.md
[14]: Google%20Maps/README.md
[16]: London%20Underground/README.md
[17]: Twitter%20Network/README.md
[18]: field_simulation.md
[19]: field_simulation.md
[20]: https://dev.twitter.com
[21]: https://openexchangerates.org/documentation










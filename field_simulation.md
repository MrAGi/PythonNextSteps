#Field Simulation

##Introduction
The field simulation task provides a way to introduce both object-oriented and event-driven programming and in addition it will enable you to discuss simulation with your students.

Finally, there are resources to help you create a distributable version of your program.

##Specification Points
This task could be used to assist in the delivery of the following specification points:

- **AQA** 3.3.1 Problem Solving
    - Information hiding and abstraction
- **AQA** 3.3.2 Programming Concepts
    - Object-oriented programming
    - Event-driven programming
    - Simulations
- **OCR** 3.3.6 High-level language programming paradigms

##Requirements

This task requires the following to be installed:

- [PyQt4][10]
- [cx_Freeze][11]

##Assumptions

Beyond having a good understanding of:

- Variables
- Selection
- Iteration
- Lists
- Functions
- File handling

there are no additional requirements for this task.

##Functionality
In this task you will create representation of crops and animals that will grow depending on the light, water and food available to them. These crops and animals can be placed in fields (which you will also create) and then finally you will produce a graphical user interface that can be used to interact with your basic simulation.

![][1]

##Design
This task is discussed and developed in detail on the [Python School][2] website.

##Code
You can find the code for the various parts of this assignment on GitHub:

- [Object-oriented materials][3]
- [Graphical Crop materials][4]
- [Graphical Field materials][5]

##Further reading

There are two books available on PyQt:

- Harwani, B. M., 2012. [*Introduction to Python Programming and Developing GUI Applications with PyQT*][6]. Boston: Course Technology.
- Summerfield, M. 2008. [*RapidGUI Programming with Python and Qt*][7]. New York: Prentice Hall.

Both of them have some useful content but the Summerfield book in particular is quite dated and does not include some of the recent improvements to PyQt. 

I would suggest that if you have worked through the [Python School][8] materials on PyQt then the [PyQt Class reference][9] is a better resource.

[1]: images/field.png
[2]: http://www.pythonschool.net
[3]: https://github.com/pythonschool/ObjectOrientedResources
[4]: https://github.com/pythonschool/GraphicalFieldSimulation
[5]: https://github.com/pythonschool/GraphicalCropSimulation
[6]: http://www.amazon.co.uk/Introduction-Python-Programming-Developing-Applications/dp/1435460979/ref=sr_1_1?ie=UTF8&qid=1369599681&sr=8-1&keywords=Introduction+to+Python+Programming+and+Developing+GUI+Applications+with+PyQT
[7]: http://www.amazon.co.uk/Rapid-GUI-Programming-Python-Development/dp/0132354187/ref=sr_1_sc_1?s=books&ie=UTF8&qid=1369599777&sr=1-1-spell&keywords=RapidGUI+Programming+with+Python+and+Qt
[8]: http://www.pythonschool.net/eventdrivenprogramming/
[9]: http://pyqt.sourceforge.net/Docs/PyQt4/classes.html
[10]: ../installing.md#pyqt4
[11]: ../installing.md#cx_freeze


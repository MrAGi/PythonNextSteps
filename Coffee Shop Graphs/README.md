#Coffee Shop

##Introduction

The Coffee Shop task provides a way of introducing relational databases to students. The concept could be used to teach topics such as:

- Entity relationship modelling
- Database design and normalisation techniques
- Querying a database with SQL
- Data definition language

However, here the focus is on reporting from an existing database. Many students choose practical projects based around databases and whilst they can construct and use these databases successfully they struggle to provide a way to report information clearly from the stored data.

You will query the database to find out the following:

- Total product sales for a particular day

This information will then be used to create and present graphs to show:

- The total sales (in pounds) of each product for the day
- The total percentage of sales that each product was responsible for

You can imagine that graphs of this sort would be useful for providing a quick overview of how the business was doing on a particular day without having to interpret the raw figures.

##Specification Points

This task could be used to assist in the delivery of the following specification points:

- **AQA** 3.3.5 Databases
    - Conceptual data model
    - Entity relationship modelling
    - Database design and normalisation techniques
    - Relational databases
    - Querying a database (SQL)
    - Data definition language (DDL)
- **OCR** 3.3.9 Databases
    - Database design
    - Normalisation and data modelling
    - Methods and tools for analysing and implementing database design
    - Use of structured query language (SQL)

In addition the task allows for further consolidation of:

- **AQA** 3.3.2 Programming Concepts
    - Object-oriented programming
    - Event-driven programming
- **OCR** 3.3.6 High-level language programming paradigms

##Requirements

This task requires the following to be installed:

- [PyQt4][27]
- [Matplotlib][28]
- [Numpy][29]

##Assumptions

This task makes the following assumptions about prior learning and experience:

- You are comfortable with database theory (see specification points above)
- You can use SQL to query a database in Python
- You have done some object-oriented programming in Python
- You have done some event-driven programming with PyQt
- You understand how to create and use dictionaries

##Functionality

This program presents the user with a graphical user interface that they can use to select a database from their file system.

![][16]

It then uses this database to provide the data for two tabs in the interface which will show different graphs.

![][17] 
![][18]

##Design

To create this program we need to create three classes:

1. A database controller
2. A widget to create the graph
3. A main window

###Database controller

The database controller has a single job - control access to the database. Rather than write code wherever we need access to the database it makes sense to centralise it all in one place. This makes it easy to track down errors or to expand the functionality available (without duplicating code)

The code for the database controller is:

    class CoffeeShopController:
        def __init__(self,path):
            self.path = path

        def query(self,sql,parameters=None):
            with sqlite3.connect(self.path) as self.db:
                cursor = self.db.cursor()
                cursor.execute("PRAGMA foreign_keys = ON")
                if parameters != None:
                    cursor.execute(sql,parameters)
                else:
                    cursor.execute(sql)
                results = cursor.fetchall()
                return results

        def product_totals(self,date):
            sql = """SELECT product.name, sum(product.price) as total
                    FROM product, order_items, customer_order
                    WHERE order_items.order_id = customer_order.order_id and 
                    order_items.product_id = product.product_id and
                    customer_order.date = ?
                    GROUP BY product.name"""
            return self.query(sql,[date])

####`__init__()` method
The constructor **`init()`** method takes a single parameter, which is the path to the database on the file system. This is stored so that is can be accessed repeatedly in the `self.path` attribute.

####`query()` method
The **`query()`** method exists as you will be repeatedly performing this operation. By creating a `query()` method you can write the code once and make sure it works rather than having similar code existing in several places (therefore several places where errors can creep in). This is the number one cause of errors when working with databases in Python so it makes sense to write it once and then forget about it.

There is one interesting thing to note about the `query()` method:

1. It makes use of the **`with`** statement

If you have not seen the `with` statement before it provides a very clean way to open and close files. You can read more about it [here][19].

####`product_totals()` method
The **`produce_totals()`** method provides a convenience method to return the daily totals for each product on a given day. It is not strictly necessary as the same query could be passed directly to `query()` but it is much nicer way to get this information. There is a discussion to be had here about interfaces, abstraction and information hiding.

###Graph Widget
To make use of **matplotlib** in a PyQt graphical user interface it must provided as a *widget* that can be placed like any other PyQt widget. The lines:

    from matplotlib.figure import Figure
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

import the functionality necessary to do this. The key thing to understand here is that `FigureCanvas` is the base class for any graphs that you want to create in the same way that `QMainWindow` is the base class for any windows you need. Therefore, you should subclass `FigureCanvas` to get the functionality you need.

    class CoffeeCanvas(FigureCanvas):
        def __init__(self):
            self.fig = Figure()
            self.ax = self.fig.add_subplot(1,1,1)
            super().__init__(self.fig)
            self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
            self.fig.canvas.draw()

        def show_bar_graph(self,data,date):
            self.ax.clear()
            data_dict = dict(data)
            for i, key in enumerate(data_dict):
                self.ax.bar(i,data_dict[key])
            self.ax.set_xticks(np.arange(len(data_dict))+0.4)
            self.ax.set_xticklabels(list(data_dict.keys()))
            self.fig.autofmt_xdate()
            self.ax.set_title("Total Sales for {0}".format(date))
            self.ax.set_xlabel("Product")
            self.ax.set_ylabel("Amount (£)")
            self.fig.canvas.draw()

        def show_pie_chart(self,data,date):
            self.ax.clear()
            data_dict = dict(data)
            data = list(data_dict.values())
            labels = list(data_dict.keys())
            self.ax.pie(data,labels=labels,autopct='%1.1f%%')
            self.ax.set_title("Percentage Sales for {0}".format(date))
            self.fig.canvas.draw()

Notice, that we have sub-classed `FigureCanvas` to create our **`CoffeeCanvas`** widget. 

####`__init__()` method
In the constructor **`init()`** method the first two lines are:

        self.fig = Figure()
        self.ax = self.fig.add_subplot(1,1,1)

`self.fig = Figure()` creates the 'page' on which you will draw the graph. `self.ax = self.fig.add_subplot(1,1,1)` creates the axis for the particular graph you want to create. It is possible to have multiple subplots on a single figure. The values `1,1,1` refer to how many rows and columns there are on the figure and the final number refers to the individual figure plot number. 

The rest of the constructor **`init()`** method looks as follows:

        super().__init__(self.fig)
        self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.fig.canvas.draw()

Normally the call to `super().__init__()` is the first call in the constructor but because it requires the figure to be passed as a parameter it has to wait until after we have set this. ` self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)` just lets PyQt know that the widget should expand in both x and y directions as the size of the window increases. Finally, the `self.fig.canvas.draw()` draws whatever we have so that it is visible.

####`show_bar_graph()` method
This method constructs a bar graph from the provided data. 

        self.ax.clear()

The first line `self.ax.clear()` clears any previous data from our subplot.

        data_dict = dict(data)
        for i, key in enumerate(data_dict):
            self.ax.bar(i,data_dict[key])

The data that is returned from **sqlite3** when querying for the `product_totals()` is provided as a **list of tuples**. To make it easier to work with we convert this data to a **dictionary** with the line `data_dict = dict(data)`.

The `for` loop constructs the bar graph. The `enumerate()` function takes the dictionary `data_dict` and returns a count value along with the key for each iteration of the loop. `self.ax.bar(i,data_dict[key])` creates a single bar on the graph, with i representing the bar number and `data_dict[key]` providing the value to use for the bar height.

The next three lines of the method are:

        self.ax.set_xticks(np.arange(len(data_dict))+0.4)
        self.ax.set_xticklabels(list(data_dict.keys()))
        self.fig.autofmt_xdate()

`self.ax.set_xticks(np.arange(len(data_dict))+0.4)` sets the position for each of the 'ticks' on the x-axis. It uses a list generated by finding the length of the `data_dict` and then generating a range from this ([0 1 2 3 4 5 6 7]) and adding 0.4 to each item in the list to center the ticks under each bar (the default width of a bar is 0.8).

`self.ax.set_xticklabels(list(data_dict.keys()))` sets the labels of each tick to the corresponding key of the dictionary. Finally, `self.fig.autofmt_xdate()` formats the labels so that they do not overlap along the axis.

The final lines of code for the method are more obvious:

        self.ax.set_title("Total Sales for {0}".format(date))
        self.ax.set_xlabel("Product")
        self.ax.set_ylabel("Amount (£)")
        self.fig.canvas.draw()

The final line `self.fig.canvas.draw()` redraws the widget with the new graph data.

####`show_pie_chart()` method
This method constructs a pie chart from the provided data.

        self.ax.clear()
        data_dict = dict(data)
        data = list(data_dict.values())
        labels = list(data_dict.keys())

The above lines are similar to those from the `show_bar_graph` method - the final two of those lines generate lists of the values and keys from the dictionary.

Then we have:

        self.ax.pie(data,labels=labels,autopct='%1.1f%%')
        self.ax.set_title("Percentage Sales for {0}".format(date))
        self.fig.canvas.draw()

`self.ax.pie(data,labels=labels,autopct='%1.1f%%')` creates the actual pie chart on our figure subplot using the provided data and labels. The `autopct='%1.1f%%'` basically formats the data values to 1 decimal place and adds the percentage symbol.

###The main window
The main window code is not particularly interesting, it is very similar to any PyQt graphical interface but it does contain instances of our `CoffeeCanvas` widgets.

####`__init__()` method
The main window constructor creates all of the required widgets and organises them appropriately.

        def __init__(self):
            super().__init__()

            self.setWindowTitle("Graphing Examples")

            self.menu_bar = QMenuBar()
            self.tool_bar = QToolBar("Manage Databases")
            self.tab = QTabWidget()

            self.bar_canvas = CoffeeCanvas()
            self.pie_canvas = CoffeeCanvas()


            self.menu_bar = QMenuBar()
            self.file_menu = self.menu_bar.addMenu("File")
            self.open_database = self.file_menu.addAction("Open Database")

            self.bar_layout = QVBoxLayout()
            self.bar_layout.addWidget(self.bar_canvas)
            self.bar_widget = QWidget()
            self.bar_widget.setLayout(self.bar_layout)

            self.pie_layout = QVBoxLayout()
            self.pie_layout.addWidget(self.pie_canvas)
            self.pie_widget = QWidget()
            self.pie_widget.setLayout(self.pie_layout)

            self.tab.addTab(self.bar_widget,"Total Sales")
            self.tab.addTab(self.pie_widget,"Percentage Sales")

            self.tool_bar.addAction(self.open_database)
            self.addToolBar(self.tool_bar)
            self.setUnifiedTitleAndToolBarOnMac(True)

            self.setMenuWidget(self.menu_bar)
            self.setCentralWidget(self.tab)

            #connections
            self.open_database.triggered.connect(self.load_database)

Most of this code you will have seen before so it will not be explained.

####`load_database()` method

        def load_database(self):
            path = QFileDialog.getOpenFileName(caption="Open Database")
            self.coffee_controller = CoffeeShopController(path)
            self.graph_data()

The load database method presents the user with a dialog window that they can use to select a file from their computer. This dialog returns the file path which is then used to create an instance of the `CoffeeShopController` class.

####`graph_data()` method
        def graph_data(self):
            totals = self.coffee_controller.product_totals("2013-05-27")
            self.pie_canvas.show_pie_chart(totals,"2012-05-27")
            self.bar_canvas.show_bar_graph(totals,"2012-05-27")

The `graph_data()` method gets the required data from the database by calling the `product_totals()` method of the `CoffeeShopController` instance. This data is then passed to the appropriate method of each of the `CoffeeCanvas` instances to create the actual graphs.

##Code

You can find the code for this task on [GitHub][20].

##Further reading

Matplotlib is a huge library at it would be impossible to give more than a basic introduction here. I would recommend the following book on the topic:

- Tosi, S. 2009. [*Matplotlib for Python Developers*][21]. Birmingham: Packt.

I would suggest that the above book is the place to start but there is [documentation for matplotlib][22] available online.

There are two books available on PyQt:

- Harwani, B. M., 2012. [*Introduction to Python Programming and Developing GUI Applications with PyQT*][23]. Boston: Course Technology.
- - Summerfield, M. 2008. [*RapidGUI Programming with Python and Qt*][24]. New York: Prentice Hall.

Both of them have some useful content but the Summerfield book in particular is quite dated and does not include some of the recent improvements to PyQt. 

I would suggest that if you have worked through the [Python School][25] materials on PyQt then the [PyQt Class reference][26] is a better resource.

[16]: ../images/opening_database.png
[17]: ../images/bar_chart.png
[18]: ../images/pie_chart.png
[19]: http://www.diveintopython3.net/files.html
[20]: http://www.github.com/MrAGi/NewAdventuresinPython/
[21]: http://www.amazon.co.uk/Matplotlib-Python-Developers-S-Tosi/dp/1847197906/ref=sr_1_1?s=books&ie=UTF8&qid=1369599806&sr=1-1&keywords=Matplotlib+for+Python+Developers
[22]: http://matplotlib.org/contents.html
[23]: http://www.amazon.co.uk/Introduction-Python-Programming-Developing-Applications/dp/1435460979/ref=sr_1_1?ie=UTF8&qid=1369599681&sr=8-1&keywords=Introduction+to+Python+Programming+and+Developing+GUI+Applications+with+PyQT
[24]: http://www.amazon.co.uk/Rapid-GUI-Programming-Python-Development/dp/0132354187/ref=sr_1_sc_1?s=books&ie=UTF8&qid=1369599777&sr=1-1-spell&keywords=RapidGUI+Programming+with+Python+and+Qt
[25]: http://www.pythonschool.net/eventdrivenprogramming/
[26]: http://pyqt.sourceforge.net/Docs/PyQt4/classes.html
[27]: ../installing.md#pyqt4
[28]: ../installing.md#matplotlib
[29]: ../installing.md#numpy
[30]: ../installing.md#network-x
[31]: ../installing.md#cx_freeze
[32]: ../installing.md#python-twitter


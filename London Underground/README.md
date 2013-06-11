#London Underground

##Introduction
The tube task provides an introduction to graphs, it can be used to illustrate key terms such as vertex, edge, neighbour, degree, path and cycle. 

In this task you will produce a representation of a part of the London Underground and then use this representation to generate directions between stations.

##Specification Points
This task could be used to assist in the deliver of the following specification points:

- **AQA** 3.3.2 Programming concepts
    - Graphs
- **OCR** 3.3.5 Data structures and data manipulation
    - Implementation of data structures, including stacks, queues and trees

In addition the task allows for further consolidation of:

- **AQA** 3.3.2 Programming Concepts
    - Object-oriented programming
    - Event-driven programming
- **OCR** 3.3.6 High-level language programming paradigms

##Requirements

This task requires the following to be installed:

- [PyQt4][52]
- [Matplotlib][53]
- [Numpy][54]
- [Network X][55]

##Assumptions
This task makes the following assumptions about prior learning and experience:

- You have some understanding of object-oriented programming
- You have some understanding of event-driven programming with PyQt4
- You have some experience of using Matplotlib

##Functionality
This program will load a preset list of stations from a CSV file and then convert this list to a graph representation. This will be displayed in a graphical user interface. 

![][41]

The user will be able to select a starting station and a destination station from drop down menus and have a route generated between them. These directions will be displayed as text and represented graphically to the user.

![][42]

##Design
There are two parts to this task:

1. A program to create the graph representation
2. A program which makes use of this representation to present the directions interface to the user.

###tube.py
The tube.py program consists of a class that is used to represent the various tube lines (and stations) as a graph and provides the methods necessary to make use of this representation.

        import networkx as nx
        import matplotlib.pyplot as plt
        import numpy
        import csv

        class TubeMap:
            def __init__(self,file_name):
                self.map = nx.Graph()
                self.file_name = file_name
                self._get_stations()


            def _get_stations(self):
                #add the stations to the graph
                with open(self.file_name,mode="r",encoding="utf-8") as my_file:
                    reader = csv.reader(my_file)
                    #csv in format: line, line colour, station1, station2, etc.
                    for tube_line in reader:
                        self.map.add_path(tube_line[2:],data={'line':"{0}".format(tube_line[0]),'edge_color':tube_line[1]})

            def _generate_edge_colours(self,current_map):
                #create the edge_colours list 
                tube_edges = current_map.edges()
                edge_colours = []
                for edge in tube_edges:
                    edge_colours.append(current_map.get_edge_data(edge[0],edge[1])["data"]["edge_color"])
                return edge_colours

            def create_graph_plot(self,current_map):
                #generate positions for each node
                pos = nx.spring_layout(current_map,iterations=1000)
                edge_colours = self._generate_edge_colours(current_map)
                #create the matplotlib figure
                plt.figure()
                #draw the graph
                nx.draw_networkx_nodes(current_map,pos,node_size=100,scale=3,node_color='w')
                nx.draw_networkx_edges(current_map,pos,edge_color=edge_colours,width=5.0)
                nx.draw_networkx_labels(current_map,pos)
                #show the plotted figure
                plt.show()

            def display_full_map(self):
                self.create_graph_plot(self.map)

            def display_travel_map(self,start,end):
                short_path = nx.shortest_path(self.map,start,end)
                travel_map = self.map.subgraph(short_path)
                self.create_graph_plot(travel_map)

            def get_directions(self,start,end):
                #get shortest path between the stations
                short_path = nx.shortest_path(self.map,start,end)

                #get the edges for the path
                edges_in_path = zip(short_path,short_path[1:])
                edges_in_path = list(edges_in_path)

                #get the line name for each edge between the start and end stations
                line = []
                for edge in edges_in_path:
                    line.append(self.map.get_edge_data(edge[0],edge[1])["data"]["line"])

                #generate the directions
                directions = []
                directions.append("Directions")
                directions.append("From {0} take the {1} line towards {2}".format(short_path[0],line[0],short_path[1]))
                current_line = line[0]
                for next_edge in range(len(edges_in_path)):
                    if line[next_edge] != current_line:
                        directions.append("Transfer to the {0} line at {1}".format(line[next_edge],short_path[next_edge]))
                        current_line = line[next_edge]
                directions.append("Alight at {0}".format(short_path[-1]))
                return directions

The first four lines import the required libraries for this program. There are then several methods which need to be explained.

####`__init__()` method
The constructor method initialises the graph (`self.map`) and stores the path to the csv file containing the list of lines and stations. The constructor then calls the `_get_stations()` method to add the necessary values to the map.

        class TubeMap:
            def __init__(self,file_name):
                self.map = nx.Graph()
                self.file_name = file_name
                self._get_stations()

####`_get_stations()` method
The `_get_stations()` method opens the csv file and then for each line of the file adds a **path** containing all of the stations to the graph. 

        def _get_stations(self):
            #add the stations to the graph
            with open(self.file_name,mode="r",encoding="utf-8") as my_file:
                reader = csv.reader(my_file)
                #csv in format: line, line colour, station1, station2, etc.
                for tube_line in reader:
                    self.map.add_path(tube_line[2:],data={'line':"{0}".format(tube_line[0]),'edge_color':tube_line[1]})

Notice, that the first two items in each line are not added as part of the path but are instead added as data about the path - the tube line name (e.g. Victoria) and its colour (as a hexadecimal representation). This data is stored as a dictionary.

####`_generate_edge_colours()` method
This method generates a list containing the colours that should be given to each edge of graph based on the data that was stored in the `_get_stations()` method.

        def _generate_edge_colours(self,current_map):
            #create the edge_colours list 
            tube_edges = current_map.edges()
            edge_colours = []
            for edge in tube_edges:
                edge_colours.append(current_map.get_edge_data(edge[0],edge[1])["data"]["edge_color"])
            return edge_colours

The first two lines of this method are straightforward enough:

        tube_edges = current_map.edges()
        edge_colours = []

A list of edges is taken from the `current_map` that is passed into the method as a parameter. Then a blank list is created to hold the edge colours.

We then iterate through all of the edges and return the edge colour value that is stored in the data dictionary.

        for edge in tube_edges:
            edge_colours.append(current_map.get_edge_data(edge[0],edge[1])["data"]["edge_color"])
        return edge_colours

Finally, the list of `edge_colours` is returned.

####`create_graph_plot()` method
This method generates a visual representation of the graph and displays it to the user.

        def create_graph_plot(self,current_map):
            #generate positions for each node
            pos = nx.spring_layout(current_map,iterations=1000)
            edge_colours = self._generate_edge_colours(current_map)
            #create the matplotlib figure
            plt.figure()
            #draw the graph
            nx.draw_networkx_nodes(current_map,pos,node_size=100,scale=3,node_color='w')
            nx.draw_networkx_edges(current_map,pos,edge_color=edge_colours,width=5.0)
            nx.draw_networkx_labels(current_map,pos)
            #show the plotted figure
            plt.show()

The first line of this method generates a list of positions for each node in the graph so that they can be plotted on to the visual representation:

        pos = nx.spring_layout(current_map,iterations=1000)

There are various different layouts that are available in network x and spring is one of then. The iterations named parameter refers to how many times you want the algorithm to relax the spring so the placement of nodes are spaced further apart.

The next two lines produce a list of colours to be used to colour each edge and initialise the figure:

        edge_colours = self._generate_edge_colours(current_map)
        plt.figure()

Finally we draw various components of the graph on to the figure and then display the final representation:

        nx.draw_networkx_nodes(current_map,pos,node_size=100,node_color='w')
        nx.draw_networkx_edges(current_map,pos,edge_color=edge_colours,width=5.0)
        nx.draw_networkx_labels(current_map,pos)
        plt.show() 

####`display_full_map()` method
This is a convenience method to visualise the whole tube map

        def display_full_map(self):
            self.create_graph_plot(self.map)

####`display_travel_map()` method
This method generates the shortest path between the given stations and then produces a graph based on the list of edges returned. Finally, it calls `create_graph_plot()` to visualise the shortest path between the stations.

        def display_travel_map(self,start,end):
            short_path = nx.shortest_path(self.map,start,end)
            travel_map = self.map.subgraph(short_path)
            self.create_graph_plot(travel_map)

####`get_directions()` method
This method produces a list of text directions to tell the user how to travel between the provided stations.

The first line of this method generates a list of stations between the start and destination stations:

        short_path = nx.shortest_path(self.map,start,end)

Then from this list we generate a list of all the edges from the start to the destination stations.

        edges_in_path = zip(short_path,short_path[1:])
        edges_in_path = list(edges_in_path)

The `zip` function generates the required tuples of connected edges but it must be converted to a list using `list` as `zip` returns an iterator object, which is not useful in this situation.

Next we need to know the line for each edge that we have just generated:

        line = []
        for edge in edges_in_path:
            line.append(self.map.get_edge_data(edge[0],edge[1])["data"]["line"])

The line is taken from the data dictionary that was created when we added the paths originally.

Finally, we must create a list of directions that can be returned to the user.

        directions = []
        directions.append("Directions")
        directions.append("From {0} take the {1} line towards {2}".format(short_path[0],line[0],short_path[1]))

The above three lines are straight-forward: we create the blank list, append the heading and also a direction stating which line to get on and in what direction you should travel.

        current_line = line[0]
        for next_edge in range(len(edges_in_path)):
            if line[next_edge] != current_line:
                directions.append("Transfer to the {0} line at {1}".format(line[next_edge],short_path[next_edge]))
                current_line = line[next_edge]

Next, we set the variable to contain the current line value and then check the edges in our path to see whether we should change to a different line or not. If we are required to change then another direction is added to the list and the current line value is updated.

###`tube_pyqt_networkx.py`
The program consists of two classes which together present the user with  visual representation of the tube network and a way to get directions between stations.

####TubeCanvas Widget
The tube canvas widget is similar to other sub-classes of **FigureCanvas** that you have created previously.

#####`__init__()` method
The constructor method has some minor differences from previous sub-classes of FigureCanvas that should be noted:

        def __init__(self):
            self.fig = plt.figure(figsize=(8,5))
            self.ax = self.fig.add_subplot(1,1,1)
            super().__init__(self.fig)
            self.ax.set_axis_off()
            self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
            self.fig.canvas.draw()

Notice that `self.fig` is an instance of **`plt.figure()`** rather than **`Figure()`** which we have used previously. This is because there is currently an issue with the integration of network x and the matplotlib Figure() class. In addition, we have set the axis to be off for this graph as they are meaningless in this context.

#####`create_graph()` method
This method updates the figure to represent the graph that is passed as a parameter. Most of this functionality has been seen previously but notice how the `edge_colours` are generated:

        def create_graph(self,current_graph):
            self.ax.clear()
            pos = nx.spring_layout(current_graph,iterations=1000)
            edge_colours = [current_graph.get_edge_data(edge[0],edge[1])["data"]["edge_color"] for edge in current_graph.edges()]
            nx.draw_networkx_nodes(current_graph,pos,node_size=100,node_color='w')
            nx.draw_networkx_edges(current_graph,pos,edge_color=edge_colours,width=5.0)
            nx.draw_networkx_labels(current_graph,pos)
            self.ax.set_axis_off()
            self.fig.set_alpha(0.0)
            self.fig.canvas.draw()

This is a **list comprehension** which is a really nice way to construct a list from a set of existing data. See the section on list comprehensions for further details.

####TubeWindow Widget
The Tube Window is similar to other sub-classes of `QMainWindow` - it generates our user interface.

#####`__init__()` method
The tube window constructor creates all of the required widgets and organises them appropriately.

        def __init__(self):
            super().__init__()

            self.setWindowTitle("Tube Directions")

            self.tube_graph = TubeCanvas()
            self.directions_text = QTextEdit()

            self.tube_layout = QHBoxLayout()
            self.tube_layout.addWidget(self.tube_graph)
            self.tube_layout.addWidget(self.directions_text)

            self.menu_bar = QMenuBar()
            self.file_menu = self.menu_bar.addMenu("File")
            self.open_map = self.file_menu.addAction("Open Map")

            self.from_station_combo_box = QComboBox()
            self.to_station_combo_box = QComboBox()
            self.directions_button = QPushButton("Get Directions")
            self.from_label = QLabel("From")
            self.to_label = QLabel("To")

            self.reset_button = QPushButton("Clear Directions")

            self.directions_layout = QGridLayout()
            self.directions_layout.addWidget(self.from_label,1,1)
            self.directions_layout.addWidget(self.to_label,1,2)
            self.directions_layout.addWidget(self.from_station_combo_box,2,1)
            self.directions_layout.addWidget(self.to_station_combo_box,2,2)
            self.directions_layout.addWidget(self.directions_button,2,3)

            self.layout = QVBoxLayout()
            self.layout.addLayout(self.tube_layout)
            self.layout.addLayout(self.directions_layout)
            self.layout.addWidget(self.reset_button)

            self.main_widget = QWidget()
            self.main_widget.setLayout(self.layout)

            self.setCentralWidget(self.main_widget)

            #connections
            self.open_map.triggered.connect(self.load_map_file)
            self.directions_button.clicked.connect(self.get_directions)
            self.reset_button.clicked.connect(self.reset_map)

Most of this code you will have seen before so it will not be explained.

#####`load_map_file()` method
This method presents the user with a dialog window that they can use to select a file from their computer. This dialog returns the file path which is then used to create an instance of `TubeMap`.

        def load_map_file(self):
            path = QFileDialog.getOpenFileName(caption="Open Tube Map")
            self.tube_map = tube.TubeMap(path)
            self.display_tube_graph()
            self.set_combo_box_stations()

Once we have the instance `self.tube_map` we then call two further methods to complete the user interface.

#####`display_tube_graph` method
This is a convenience method which calls the `create_graph` method of the TubeMap instance.

        def display_tube_graph(self):
            self.tube_graph.create_graph(self.tube_map.map)

#####`set_combo_box_stations()` method
This method gets a list of the stations from the graph, sorts them into alphabetical order and then adds this list to the two combo boxes that the user will select the start and destination stations from.

        def set_combo_box_stations(self):
            stations = self.tube_map.map.nodes()
            stations.sort()
            self.from_station_combo_box.addItems(stations)
            self.to_station_combo_box.addItems(stations)

#####`get_directions()` method
This method gets the selected stations from the user interface and then finds the shortest path between them. It then uses the `get_directions` method from the instance of TubeMap to get a list of the text directions. Finally, it updates the interface to show the direction maps and calls `display_directions` method to place the text directions on the interface.

        def get_directions(self):
            from_station = self.from_station_combo_box.currentText()
            to_station = self.to_station_combo_box.currentText()
            short_path = nx.shortest_path(self.tube_map.map,from_station,to_station)
            directions = self.tube_map.get_directions(from_station,to_station)
            travel_map = self.tube_map.map.subgraph(short_path)
            self.tube_graph.create_graph(travel_map)
            self.display_directions(directions)

#####`display_directions()` method
This method converts the list of directions passed as a parameter into a HTML ordered list and then adds them to the user interface.

        def display_directions(self,directions):
            text = "<h1>{0}</h1><ol>".format(directions[0])
            for direction in directions[1:]:
                text += "<li>{0}</li>".format(direction)
            text += "</ol>"
            self.directions_text.setText(text)

#####`reset_map()` method
This method returns the visual representation of the map to the full tube map and clears any text directions present in the interface.

        def reset_map(self):
            self.tube_graph.create_graph(self.tube_map.map)
            self.directions_text.clear()

##Code

You can find the code for this task on [GitHub][43].

##Further reading

Network X has a lot more functionality that has been discussed in this task, please see its [documentation][44] for further details.

Matplotlib is a huge library at it would be impossible to give more than a basic introduction here. I would recommend the following book on the topic:

- Tosi, S. 2009. [*Matplotlib for Python Developers*][46]. Birmingham: Packt.

I would suggest that the above book is the place to start but there is [documentation for matplotlib][47] available online.

There are two books available on PyQt:

- Harwani, B. M., 2012. [*Introduction to Python Programming and Developing GUI Applications with PyQT*][48]. Boston: Course Technology.
- - Summerfield, M. 2008. [*RapidGUI Programming with Python and Qt*][49]. New York: Prentice Hall.

Both of them have some useful content but the Summerfield book in particular is quite dated and does not include some of the recent improvements to PyQt. 

I would suggest that if you have worked through the [Python School][50] materials on PyQt then the [PyQt Class reference][51] is a better resource.

[41]: ../images/tube_map_full.png
[42]: ../images/tube_map_directions.png
[43]: http://www.github.com/MrAGi/NewAdventuresinPython/
[44]: http://networkx.github.io
[46]: http://www.amazon.co.uk/Matplotlib-Python-Developers-S-Tosi/dp/1847197906/ref=sr_1_1?s=books&ie=UTF8&qid=1369599806&sr=1-1&keywords=Matplotlib+for+Python+Developers
[47]: http://matplotlib.org/contents.html
[48]: http://www.amazon.co.uk/Introduction-Python-Programming-Developing-Applications/dp/1435460979/ref=sr_1_1?ie=UTF8&qid=1369599681&sr=8-1&keywords=Introduction+to+Python+Programming+and+Developing+GUI+Applications+with+PyQT
[49]: http://www.amazon.co.uk/Rapid-GUI-Programming-Python-Development/dp/0132354187/ref=sr_1_sc_1?s=books&ie=UTF8&qid=1369599777&sr=1-1-spell&keywords=RapidGUI+Programming+with+Python+and+Qt
[50]: http://www.pythonschool.net/eventdrivenprogramming/
[51]: http://pyqt.sourceforge.net/Docs/PyQt4/classes.html
[52]: ../installing.md#pyqt4
[53]: ../installing.md#matplotlib
[54]: ../installing.md#numpy
[55]: ../installing.md#network-x
[56]: ../installing.md#cx_freeze
[57]: ../installing.md#python-twitter






        
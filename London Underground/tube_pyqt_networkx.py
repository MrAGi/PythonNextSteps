import sys
import pickle

import networkx as nx
import numpy as np

from PyQt4.QtGui import *

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

import tube

class TubeCanvas(FigureCanvas):
    def __init__(self):
        self.fig = plt.figure(figsize=(8,5))
        self.ax = self.fig.add_subplot(1,1,1)
        super().__init__(self.fig)
        self.ax.set_axis_off()
        self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.fig.canvas.draw()

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


class TubeWindow(QMainWindow):
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

    def load_map_file(self):
        path = QFileDialog.getOpenFileName(caption="Open Tube Map")
        self.tube_map = tube.TubeMap(path)
        self.display_tube_graph()
        self.set_combo_box_stations()

    def display_tube_graph(self):
        self.tube_graph.create_graph(self.tube_map.map)

    def set_combo_box_stations(self):
        stations = self.tube_map.map.nodes()
        stations.sort()
        self.from_station_combo_box.addItems(stations)
        self.to_station_combo_box.addItems(stations)

    def get_directions(self):
        from_station = self.from_station_combo_box.currentText()
        to_station = self.to_station_combo_box.currentText()
        short_path = nx.shortest_path(self.tube_map.map,from_station,to_station)
        directions = self.tube_map.get_directions(from_station,to_station)
        travel_map = self.tube_map.map.subgraph(short_path)
        self.tube_graph.create_graph(travel_map)
        self.display_directions(directions)

    def display_directions(self,directions):
        print(directions)
        text = "<h1>{0}</h1><ol>".format(directions[0])
        for direction in directions[1:]:
            text += "<li>{0}</li>".format(direction)
        text += "</ol>"
        self.directions_text.setText(text)

    def reset_map(self):
        self.tube_graph.create_graph(self.tube_map.map)
        self.directions_text.clear()


if __name__ == "__main__":
    application = QApplication(sys.argv)
    main_window = TubeWindow()
    main_window.show()
    main_window.raise_()
    application.exec_()
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
        nx.draw_networkx_nodes(current_map,pos,node_size=100,node_color='w')
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

if __name__ == "__main__":
    tube_map = TubeMap("tube.csv")
    tube_map.display_full_map()
    directions = tube_map.get_directions("Kentish Town","Knightsbridge")
    print(directions)
    tube_map.display_travel_map("Kentish Town","Knightsbridge")



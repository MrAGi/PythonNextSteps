import pickle
import networkx as nx
import matplotlib.pyplot as plt
import numpy
import random

#create a new directed graph
twitter_graph = nx.DiGraph()

#open file with follower data
with open("twitter_follower_directed.dat",mode="rb") as my_file:
    data = pickle.load(my_file)

#get follower data from the dictionary
follower_data = data['data']
#set key user
main_user = "adammcnicol"

#add the nodes and edges
for follower in follower_data.values():
    screen_name = follower["screen_name"]
    connections = follower["connections"]
    for connection in connections:
        if connection == "followed_by":
            twitter_graph.add_edge(screen_name, main_user)
        elif connection == "following":
            twitter_graph.add_edge(main_user,screen_name)

#get positions for each of the nodes in the graph
pos = nx.spring_layout(twitter_graph)

#tweak the positioning of the nodes which are directed both ways
for node, value in pos.items():
    if twitter_graph.has_edge(main_user, node) and twitter_graph.has_edge(node,main_user):
        if value[0] > pos[main_user][0]:
            value[0] = value[0] + (random.randrange(1,4,1)/10)
        else:
            value[0] = value[0] - (random.randrange(1,4,1)/10)
        if value[1] > pos[main_user][1]:
            value[1] = value[1] + (random.randrange(1,4,1)/10)
        else:
            value[1] = value[1] - (random.randrange(1,4,1)/10)

#create the matplotlib figure
plt.figure(figsize=(25,10))

#draw the graph
nx.draw_networkx_nodes(twitter_graph,pos,node_size=200,with_labels=False)
nx.draw_networkx_edges(twitter_graph,pos,alpha=0.3)

#alter positioning for labels
# for node, value in pos.items():
#     value[0] -= 0.05

#add the labels
nx.draw_networkx_labels(twitter_graph,pos)

#show the figure
plt.show()

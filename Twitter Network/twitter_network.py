import pickle
import networkx as nx
import matplotlib.pyplot as plt
import numpy

main_user = "adammcnicol"
twitter_graph = nx.Graph()

#produce the graph for the followers of the main user
with open("twitter_network.dat",mode="rb") as my_file:
    graph_data = pickle.load(my_file)
    follower_user_data = graph_data["follower_user_data"]#followers of followers screen_names
    followers = graph_data["followers"] #my followers
    followers_screen_names = graph_data["followers_screen_names"] #screen_names of my followers
    follower_data = graph_data["follower_data"]  #followers of followers

for follower in followers_screen_names:
    twitter_graph.add_edge(main_user,follower["screen_name"].lower())
    for each,value in follower_user_data.items():
        for name in value:
            twitter_graph.add_edge(follower["screen_name"].lower(),name["screen_name"].lower())

# #set positions
pos = nx.random_layout(twitter_graph)

plt.figure(figsize=(16,10))

nx.draw_networkx_nodes(twitter_graph,pos,node_size=30)
nx.draw_networkx_edges(twitter_graph,pos,alpha=0.01)

#get the nodes that we want to draw labels for
clique = nx.cliques_containing_node(twitter_graph,nodes=[main_user])
clique = clique[main_user][0]
clique.append(main_user)
labels = {}
for name in clique:
    labels[name] = name
nx.draw_networkx_labels(twitter_graph,pos,font_size=16,labels=labels)
plt.show()

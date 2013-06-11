#Twitter Network

##Introduction
The Twitter network task provides another opportunity to work with graphs, APIs, object-oriented programming and event-driven programming.

In this task you will collect data on your twitter followers (and their followers) and represent this as a graph.

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

- [PyQt4][58]
- [Matplotlib][59]
- [Numpy][60]
- [Network X][61]
- [Python Twitter][63]

##Assumptions
This task makes the following assumptions about prior learning and experience:

- You have some understanding of object-oriented programming
- You have some understanding of event-driven programming with PyQt4
- You have some experience of using Matplotlib

##Functionality
This task is split into two sections:

1. Gathering the required data from twitter
2. Using this data to create a graph

Gathering the data may take some time depending on the number of followers you have as there is a limit on the number of requests that can be made to the Twitter API in every 15 minute period.

However, once you have the data generating the graph is quite straight-forward.

![][52]

##Design
Before starting this task you require a [developer account][53] with Twitter and you must have created a new application to get a **consumer key** and **consumer secret**. Without these you will not be able to gather any data from Twitter. 

Please see the section on creating a Twitter developer account for further details.

###`twitter_network_gather_data.py`
The program contains a class that can be instantiated to gather data about your followers and then save this information to a file for later use.

####TwitterData class
The TwitterData class enables you to connect to the Twitter API and return information about your followers.

#####`__init__()` method
The constructor method sets the values for the consumer key and secret and authorises the application to use your twitter account.

        def __init__(self):
            self.consumer_key = "see documentation"
            self.consumer_secret = "see documentation"

            self.oauth_filename = 'twitter_oauth'

            if not os.path.exists(self.oauth_filename):
                twitter.oauth_dance("see documentation", self.consumer_key, self.consumer_secret, self.oauth_filename)

            self.oauth_token, self.oauth_token_secret = twitter.read_token_file(self.oauth_filename)

Remember that you must have values for `self.consumer_key` and `self.consumer_secret` - these are found in the applications section of your Twitter developer account. In addition, you must have an application name to provide to the `twitter.oauth_dance` method which authorises your particular application to use your twitter account.

#####`login()` method
This method logs into the Twitter API using the credentials that have either been created in the `__init__()` method or loaded from a file if authorisation had been granted previously.

        def login(self):
            self.auth = twitter.OAuth(self.oauth_token, self.oauth_token_secret, self.consumer_key, self.consumer_secret)
            self.twitter_api = twitter.Twitter(domain="api.twitter.com",
                                  api_version='1.1',
                                  auth=self.auth)

#####`get_followers()` method
This method returns your followers (if `user_id` = None) or it can return the followers of another user if the `user_id` value is set.

        def get_followers(self,user_id=None):
            followers = self.twitter_api.followers.ids(user_id=user_id)
            return followers['ids']

#####`get_user_data()` method
This method returns all the data twitter has about a particular user id. A list of up to 100 users can be sent as the `user_id`.

        def get_user_data(self,user_ids):
            user_data = self.twitter_api.users.lookup(user_id=user_ids)


            return list(user_data)

####`get_all_followers()` function
This function is designed to get the follower information for each of your own followers. The Twitter API allows only 15 requests for this information per 15 minute period therefore it is designed to work around this constraint by sleeping for 15 minutes after it reaches this threshold. 

        def get_all_followers(tw,followers):
            follower_data = {}
            api_calls = 0
            for follower in followers:
                try:
                    f = tw.get_followers(user_id=follower)
                    follower_data[str(follower)] = f
                except twitter.api.TwitterHTTPError:
                    print("User {0} does not authorise you to view their followers".format(follower))
                api_calls += 1
                if api_calls == 15:
                    print("maximum api calls reached - sleeping for 15 minutes")
                    timer = 15
                    while timer > 0:
                        print("{0} minutes remaining".format(timer))
                        time.sleep(60)
                        timer -= 1
            return follower_data

Obviously the more followers you have the longer this operation is going to take. In addition, some of your followers may not allow you to gather this information on them so there is error handling in place to deal with this situation.

It will construct a dictionary called `follower_data` where each key is the user_id of one of your followers and the associated value will be a list containing the user ids of each of their followers.

####`get_all_user_data()` function
This function is designed get all of the user information for each of your followers followers. 

        def get_all_user_data(tw,followers):
            user_data = {}
            for key, value in followers.items():
                print("the key is {0}".format(key))
                if len(value) > 0:
                    print(value)
                    f = tw.get_user_data(str(value[:100]).strip("[]")) 
                else:
                    f = None
                user_data[str(key)] = f
            return user_data

For each item in the **followers** dictionary (which is a key representing one of your followers and a value containing a list of their followers) the user data is requested from twitter.

Notice, that you must convent the list of  users id to a string to pass it to the `get_user_data` method:

    f = tw.get_user_data(str(value[:100]).strip("[]")

In addition, because there is a limit of 100 user objects that can be returned in a single request the length of the list has been trimmed to match. This means that we do not need to have multiple requests for each of your followers.

####`main()` function
The main function is responsible for controlling the operation of the program. The first two lines instantiate a TwitterData object and then use it to log into the API:

        twitter_data = TwitterData()
        twitter_data.login() 

It then gets all of your followers user ids and uses this data to get the rest of the information about your followers:

        followers = twitter_data.get_followers()
        followers_screen_names = twitter_data.get_user_data(str(followers[:30]).strip("[]")) 

Notice, that followers has been limited to 30 so that we do not have to wait more that 15 minutes for our data.

Then we get the followers of each of your followers user ids and then use this data to get the rest of the information about them:

        follower_data = get_all_followers(twitter_data,followers[:30])
        follower_user_data = get_all_user_data(twitter_data, follower_data)

Finally, all of the collected information is placed in a dictionary and saved to a file:

        file_data = {'followers': followers[:30], 'followers_screen_names': followers_screen_names,
                'follower_data': follower_data, 'follower_user_data':follower_user_data}

        with open("twitter_network.dat",mode="wb") as my_file:
            pickle.dump(file_data,my_file)
            print("data saved")

###`twitter_network.py`
This program generates a graph to show the connections between people in your twitter network.

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
        clique = nx.cliques_containing_node(twitter_graph,nodes=["adammcnicol"])
        clique = clique["adammcnicol"][0]
        clique.append("adammcnicol")
        labels = {}
        for name in clique:
            labels[name] = name
        nx.draw_networkx_labels(twitter_graph,pos,font_size=16,labels=labels)

        plt.show()

The first two lines sets who you are (as it is a graph of your twitter network) and creates an instance of a simple graph:

        main_user = "adammcnicol"
        twitter_graph = nx.Graph()

Then the information that was saved previous is loaded:

        with open("twitter_network.dat",mode="rb") as my_file:
            graph_data = pickle.load(my_file)
            follower_user_data = graph_data["follower_user_data"]
            followers = graph_data["followers"] 
            followers_screen_names = graph_data["followers_screen_names"]
            follower_data = graph_data["follower_data"]

The graph is then constructed by iterating through the user objects stored in the **follower_screen_names** dictionary:

        for follower in followers_screen_names:
            twitter_graph.add_edge(main_user,follower["screen_name"].lower())
            for each,value in follower_user_data.items():
                for name in value:
                    twitter_graph.add_edge(follower["screen_name"].lower(),name["screen_name"].lower()) 

Once the graph is constructed we calculate positions for each node and then plot the nodes and edges:

        pos = nx.random_layout(twitter_graph)
        plt.figure(figsize=(16,10))
        nx.draw_networkx_nodes(twitter_graph,pos,node_size=30)
        nx.draw_networkx_edges(twitter_graph,pos,alpha=0.01)

Notice, that the edges are draw very lightly (alpha value of 0.01) this means that it is easy to see users that have lots of connections - as the lines build up on to off each other the impression is of a darker line. 

Finally, because there are so many nodes we don't want to label them all (otherwise we would see nothing but labels) we use the `clique` function to return a list of nodes connected to our main user:

    clique = nx.cliques_containing_node(twitter_graph,nodes=[main_user])
    clique = clique[main_user][0]
    clique.append(main_user)
    labels = {}
    for name in clique:
        labels[name] = name
    nx.draw_networkx_labels(twitter_graph,pos,font_size=16,labels=labels)
    plt.show()

Once we have this list we can plot the labels and show the completed graph.

##Code

You can find the code for this task on [GitHub][54].

##Further reading

Network X has a lot more functionality that has been discussed in this task, please see its [documentation][55] for further details.

Matplotlib is a huge library at it would be impossible to give more than a basic introduction here. I would recommend the following book on the topic:

- Tosi, S. 2009. [*Matplotlib for Python Developers*][56]. Birmingham: Packt.

I would suggest that the above book is the place to start but there is [documentation for matplotlib][57] available online.

[52]: ../images/twitter_followers.png
[53]: https://dev.twitter.com
[54]: http://www.github.com/MrAGi/NewAdventuresinPython/
[55]: http://networkx.github.io
[56]: http://www.amazon.co.uk/Matplotlib-Python-Developers-S-Tosi/dp/1847197906/ref=sr_1_1?s=books&ie=UTF8&qid=1369599806&sr=1-1&keywords=Matplotlib+for+Python+Developers
[57]: http://matplotlib.org/contents.html
[58]: ../installing.md#pyqt4
[59]: ../installing.md#matplotlib
[60]: ../installing.md#numpy
[61]: ../installing.md#network-x
[62]: ../installing.md#cx_freeze
[63]: ../installing.md#python-twitter

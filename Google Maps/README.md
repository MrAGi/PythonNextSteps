#Google Maps

##Introduction
The Google maps task provides a way of introducing networking concepts to students. Topics that could be introduced through this task include:

- client-server
- tcp/ip protocol stack
- sockets

In addition, this task will introduce students to interacting with external APIs (in this case the Google Maps API).

In this task you will provide an address and then the program will pass this address to the Google Maps API which will return the GPS co-ordinates for that address. 

There are three variations of this task:

1. Using the **`urllib`** library (reasonably high level)
2. Using the **`httplib`** library (lower level)
3. Using the **`socket`** library (lower still)

By looking at the same task in three different ways you can see how the the functionality we expect from programs is built up in layers and that the lower the layer the more you have to do yourself to get everything working.

In addition to discussing networking, this task could be useful in discussing information hiding and abstraction.

##Specification Points
This task could be used to assist in the delivery of the following specification points:

- **AQA** 3.2.5 The structure of the Internet
    - Understanding client-server
    - The TCP/IP protocol stack
    - Sockets
- **OCR** 3.1.5 Data transmission
    - Protocols
    - Networking

In addition the task allows for further consolidation of:

- **AQA** 3.3.1 Problem solving
    - Information hiding and abstraction

##Requirements
There are no additional software requirements for this task but you may need to ensure that you network is setup to allow for Python to make network connections.

##Assumptions
This task makes the following assumptions about prior learning and experience:

- You have some understanding of the [JSON][26] data format
- You can create and use Python dictionaries

##Functionality
The programs in this task are very simple, they do not require any input from the user when run and output consists of printing co-ordinates from a dictionary. Each program will send a predefined address to the Google Maps API and then process the returned information to extract the co-ordinates.

There is a possible extension task where students construct there own addresses to pass to the API and/or develop the program to have a higher-level and easier to understand interface.

##Design
There are three variations of the same basic program provided:

- google_maps.py
- google_http.py
- google_socket.py

Each program exposes functionality at a lower level that the one above until we get to google_socket.py which demonstrates how to construct a HTTP request directly (exposing the application layer of the TCP/IP protocol stack).

###google_maps.py
The google_maps.py program demonstrates how we can construct a request and send it to a server, which will process the request and send us a response.

It makes use of the [Google Geocoding API][27], which provides a method of converting addresses into geographic co-ordinates.

        import urllib.parse
        import urllib.request
        import json

        path = "http://maps.googleapis.com/maps/api/geocode/json?"

        address = "McDiarmid Park, Crieff Road, Perth, PH1 2SJ"
        parameters = {'address': address,'sensor': 'false' }

        encoded_parameters = urllib.parse.urlencode(parameters)
        url = path + encoded_parameters

        reply = urllib.request.urlopen(url).read()
        reply = json.loads(reply.decode('utf-8'))

        print(reply['results'][0]['geometry']['location'])

The above program is not terribly difficult to undersand. The first three lines import the required library and then we set the **path** variable to the address where we can send API requests on the Internet.

        address = "McDiarmid Park, Crieff Road, Perth, PH1 2SJ"
        parameters = {'address': address,'sensor': 'false' }

The above two lines set the address we are going to search for and then a dictionary is constructed containing the both the address and an additional value (**sensor**) required by the API - sensor refers to whether or not the device sending the request has location sensing hardware.

        encoded_parameters = urllib.parse.urlencode(parameters)
        url = path + encoded_parameters

We then encode the parameters into the correct format for sending across the Internet. For example, it would convert the dictionary to the following:

        sensor=false&address=McDiarmid+Park%2C+Crieff+Road%2C+Perth%2C+PH1+2SJ

The encoded parameters and then added to the path to construct the full url to be requested from the server.

        reply = urllib.request.urlopen(url).read()
        reply = json.loads(reply.decode('utf-8'))

The request is then sent and the reply is read and stored. This reply is then decoded using the json library as this was the format it was sent in. Decoding from json format returns in a data structure consisting of Python dictionaries and lists.

        print(reply['results'][0]['geometry']['location'])

This prints the co-ordinates from the reply. As you can see one of the keys in reply is **'results'** which is a list. We request the first index from the list, which is a dictionary. This dictionary has the key **'geometry'**, the value attached to this is another dictionary. Finally, we request the value attached to the **'location'** key of this dictionary to get the co-ordinates.

###google_http.py
The google_http.py program works at a lower level that google_maps.py. Rather than relying on the urllib library to manage a HTTP conversation for us we can use the http.client library directly. This means that we must have a greater understanding of the underlying protocol.

        import http.client
        import json

        path = "/maps/api/geocode/json?address=156+McDiarmid+Park%2C+Crieff+Road%2C+Perth%2C+PH1+2SJ&sensor=false"

        connection = http.client.HTTPConnection('maps.googleapis.com')
        connection.request('GET',path)
        reply = connection.getresponse().read()

        reply = json.loads(reply.decode('utf-8'))
        print(reply['results'][0]['geometry']['location'])

Notice that there is no helper function to encode the path for us this time - we must be able to do this ourselves:

        path = "/maps/api/geocode/json?address=156+McDiarmid+Park%2C+Crieff+Road%2C+Perth%2C+PH1+2SJ&sensor=false"

In addition, generating the response from the server is now more complex. Firstly we must make a connection to the server directly and then we send the request. For the request we need to know the command (**GET**) to send along with it to get the required response from the server:

        connection = http.client.HTTPConnection('maps.googleapis.com')
        connection.request('GET',path)
        reply = connection.getresponse().read()

Once we have the response the decoding part of the program is exactly the same as before:

        reply = json.loads(reply.decode('utf-8'))
        print(reply['results'][0]['geometry']['location'])

This program could be used as part of a discussion on information hiding and abstraction.

###google_socket.py
The final program in this task presents a raw network conversation and shows how the hypertext transfer protocol must be constructed to successful receive a response from a server.

        import socket

        path = "/maps/api/geocode/json?address=156+McDiarmid+Park%2C+Crieff+Road%2C+Perth%2C+PH1+2SJ&sensor=false"

        data = """GET {0} HTTP/1.1\r
        Host: maps.googleapis.com:80\r
        User-Agent: google_socket.py\r
        Connection: close\r
        \r\n""".format(path)

        data = data.encode()
        sock = socket.socket()
        sock.connect(('maps.googleapis.com',80))
        sock.sendall(data)

        reply = sock.recv(4096)
        reply = reply.decode('utf-8')
        print(reply)

Again, we must understand how to correctly format the data we wish to send to the server:

        path = "/maps/api/geocode/json?address=156+McDiarmid+Park%2C+Crieff+Road%2C+Perth%2C+PH1+2SJ&sensor=false"

In addition to this we need to understand how to construct a correctly formatted HTTP header for our request:

        data = """GET {0} HTTP/1.1\r
        Host: maps.googleapis.com:80\r
        User-Agent: google_socket.py\r
        Connection: close\r
        \r\n""".format(path)

The next few lines of code convert the strings that Python works with into bytes that can be transferred across the network, creates and opens a socket and sends all of the data to the server:

        data = data.encode()
        sock = socket.socket()
        sock.connect(('maps.googleapis.com',80))
        sock.sendall(data)

Finally, the reply is received, which we decode from bytes into an appropriate string format that we can interpret in Python:

        reply = sock.recv(4096)
        reply = reply.decode('utf-8')
        print(reply)

The line `sock.recv(4096)` refers to the maximum size of the packets (in bytes) that can be received.

This program is clearly more complex that the previous examples and can be used as an introduction to the application layer of the TCP/IP protocol stack and/or sockets.

##Code

You can find the code for this task on [GitHub][29]

##Further reading

Network programming is a interesting area and there are lots more tasks that could be constructed if you had more understanding. All of these examples have been adapted from the following book:

- Rhodes, B., Goerzen, J., 2010. [*Foundations of Python Network Programming*][30]. 2nd ed. New York: Apress.

Unfortunately, it is somewhat out of date as the samples are all in Python 2 and the Google Maps API has changed significantly since the book was published. However, there is a lot of interesting material in the book and it may be worthwhile if you are happy to spend sometime converting examples from Python 2 to Python 3.

[26]: http://www.json.org
[27]: https://developers.google.com/maps/documentation/geocoding/
[29]: http://www.github.com/MrAGi/NewAdventuresinPython/
[30]: http://www.amazon.co.uk/Foundations-Python-Network-Programming-Goerzen/dp/1590593715/ref=sr_1_1?s=books&ie=UTF8&qid=1369599759&sr=1-1&keywords=Foundations+of+Python+Network+Programming
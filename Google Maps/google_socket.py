import socket

path = "/maps/api/geocode/json?address=156+McDiarmid+Park%2C+Crieff+Road%2C+Perth%2C+PH1+2SJ&sensor=false"

data = """GET {0} HTTP/1.1\r
Host: maps.googleapis.com:80\r
User-Agent: google_socket.py\r
Connection: close\r
\r\n""".format(path)

data = data.encode()
print(data)

sock = socket.socket()
sock.connect(('maps.googleapis.com',80))
sock.sendall(data)

reply = sock.recv(4096)
reply = reply.decode('utf-8')
print(reply)
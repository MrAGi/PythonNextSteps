import http.client
import json

path = "/maps/api/geocode/json?address=156+McDiarmid+Park%2C+Crieff+Road%2C+Perth%2C+PH1+2SJ&sensor=false"

connection = http.client.HTTPConnection('maps.googleapis.com')
connection.request('GET',path)

reply = connection.getresponse().read()
print(reply)

reply = json.loads(reply.decode('utf-8'))
print(reply['results'][0]['geometry']['location'])
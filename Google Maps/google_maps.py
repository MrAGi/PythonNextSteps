import urllib.parse
import urllib.request
import json

path = "http://maps.googleapis.com/maps/api/geocode/json?"

address = "McDiarmid Park, Crieff Road, Perth, PH1 2SJ"
parameters = {'address': address,'sensor': 'false' }

encoded_parameters = urllib.parse.urlencode(parameters)
print(encoded_parameters)

url = path + encoded_parameters
#print(url)

reply = urllib.request.urlopen(url).read()
reply = json.loads(reply.decode('utf-8'))


print(reply['results'][0]['geometry']['location'])

import urllib.parse
import urllib.request
import json
import datetime

path = "http://openexchangerates.org/api/latest.json?"
app_id = "71aacd3c6da94bd7bbf3e2507c3219ac"

amount = 1

parameters = {'app_id': app_id}
parameters = urllib.parse.urlencode(parameters)
url = path + parameters
print(url)

reply = urllib.request.urlopen(url).read()
reply = json.loads(reply.decode('utf-8'))
print(reply)

date = datetime.datetime.fromtimestamp(reply['timestamp'])
print(date)

path = "http://openexchangerates.org/api/currencies.json?app_id="

url = path + app_id
reply = urllib.request.urlopen(url).read()
reply = reply.decode('utf-8')
reply = json.loads(reply)
print(reply['PGK'])
print(str(reply).encode('utf-8'))

path = "http://openexchangerates.org/api/historical/2011-11-21.json?app_id="
url = path + app_id
reply = urllib.request.urlopen(url).read()
reply = reply.decode('utf-8')
reply = json.loads(reply)
print(reply)

date = datetime.datetime.fromtimestamp(reply['timestamp'])
print(date)
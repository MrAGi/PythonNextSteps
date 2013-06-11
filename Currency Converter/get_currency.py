import urllib.request
import json
import datetime
import pickle

path = "http://openexchangerates.org/api/historical/2013-04-{0}.json?app_id="
app_id = "see documentation"
url = path + app_id

april = []

for day in range(1,31):
    if day < 10:
        full_url = url.format("0"+str(day))
    else:
        full_url = url.format(day)
    reply = urllib.request.urlopen(full_url).read()
    reply = reply.decode('utf-8')
    reply = json.loads(reply)
    print(reply)
    day_values = {'date': datetime.datetime.fromtimestamp(reply['timestamp']),
                  'base': reply['base'],
                  'GBP': reply['rates']['GBP'],
                  'USD': reply['rates']['USD'],
                  'EUR': reply['rates']['EUR'],
                  'CAD': reply['rates']['CAD'],
                  'AUD': reply['rates']['AUD'],
                  'NZD': reply['rates']['NZD'],
                  'JPY': reply['rates']['JPY'],
                  'CNY': reply['rates']['CNY'],
                  'RUB': reply['rates']['RUB']}
    april.append(day_values)

with open("april_currency_data.dat",mode="wb") as currency_file:
    pickle.dump(april,currency_file)
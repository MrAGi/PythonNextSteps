import pickle
import matplotlib.pyplot as plt
import matplotlib.dates as dte
import datetime

with open("april_currency_data.dat",mode="rb") as currency_file:
    april = pickle.load(currency_file)

CAD = []
AUD = []
GBP = []
NZD = []
JPY = []
CNY = []
RUB = []
EUR = []
dates = []

for day in april:
    CAD.append(day['CAD'])
    AUD.append(day['AUD'])
    GBP.append(day['GBP'])
    NZD.append(day['NZD'])
    JPY.append(day['JPY'])
    CNY.append(day['CNY'])
    RUB.append(day['RUB'])
    EUR.append(day['EUR'])
    dates.append(day['date'])

#plot graph
print(dates)
fig = plt.figure()
ax = fig.add_subplot(1,1,1)


ax.set_ylabel("US Dollars")
ax.set_xlabel("Date")
ax.set_title("Currency Rates in April 2013")

mpl_date = dte.date2num(dates)
days_loc = dte.DayLocator()

ax.plot_date(mpl_date,CAD,'b-')
ax.plot_date(mpl_date,AUD,'g-')
ax.plot_date(mpl_date,GBP,'r-')
ax.plot_date(mpl_date,NZD,'k-')
ax.plot_date(mpl_date,EUR,'y-')

ax.legend(["CAD","AUD","GBP","NZD","EUR"],loc="upper left")

date_fmt = dte.DateFormatter('%d/%m')
ax.xaxis.set_major_formatter(date_fmt)
ax.xaxis.set_major_locator(days_loc)
fig.autofmt_xdate(rotation=90)


plt.show()
#Currency Converter

##Introduction
A currency conversion task is one of the earliest tasks that any new programmer will attempt. It is not particularly difficult but it consolidates a range of concepts. However, generally this task will be undertaken using either made up data or having the student gather the data manually from various sources.

This could be improved by taking the data automatically from somewhere, providing an opportunity to discuss client-server principles and also we could visualise the collected data so that it is easy to interpret. 

Now instead of having a beginners exercise, you have one that can be used to look at networking, event-driven programming, object-oriented programming, file handling and charting.

##Specification Points
This task could be used to assist in the delivery of the following specification points:

- **AQA** 3.2.5 The structure of the Internet
    - Understanding client-server
- **OCR** 3.1.5 Data transmission
    - Networking

In addition the task allows for further consolidation of:

- **AQA** 3.3.2 Programming Concepts
    - Object-oriented programming
    - Event-driven programming
- **OCR** 3.3.6 High-level language programming paradigms

##Requirements
This task requires the following to be installed:

- [PyQt4][41]
- [Matplotlib][42]
- [Numpy][43]

In addition you will also need an **application id** for the following service:

- [Open Exchange Rates][31]

The free plan provides quite limited access to the exchange rate API but it is sufficient for this task.

##Assumptions
This task makes the following assumptions about prior learning and experience:

- You have some understanding of the [JSON][27] data format
- You can create and use Python dictionaries
- You have an application id with [Open Exchange Rates][31]
- You have some basic experience with matplotlib

##Functionality
There are two separate parts to this task:

1. A program to gather data and save it to a file
2. A program to display and use the data stored in the saved file

Because of the limitations placed on API usage by the free application id it means that we can only make up to a 1000 requests to the API per month. This may seem like a lot but if your program is quite buggy and you are constantly making changes to it you could easily hit this limit quite quickly. Therefore, it makes more sense to gather what we need in terms of data and save it into a file so we can use it repeatedly whilst working on the second part of the task.

The second part of the task uses the saved data to present a line graph showing how the selected currencies have fluctuated against the US Dollar over the course of a month. Again, this is a limitation of the free application id - the base currency is fixed to dollars. Finally, the task will along the user to enter an amount in one currency and have it converted into another with the result being displayed on the interface.

##Design
There are two separate parts to this task:

1. get_currency.py
2. currency_pyqt.py

###get_currency.py
This program accesses the Open Exchange Rate API and gathers data for each day of April 2013. It selects particular currencies for each day and stores them in a dictionary, which is then added to a list. Finally, this list is saved to a file.

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

The first four lines of this program import the required libraries. We then create the url needed to request currency data for each day in April:

        path = "http://openexchangerates.org/api/historical/2013-04-{0}.json?app_id="
        app_id = "see documentation"
        url = path + app_id

Notice, that you require an **`app_id`** here and that string formating syntax has been used so that we can easily reuse this url for each day in April.

The program then goes into a loop for each day of April. We then use the loop counter (**day**) to produce the full url for a particular day in April:

        if day < 10:
                full_url = url.format("0"+str(day))
            else:
                full_url = url.format(day)

Once the full url has been created the currency data is requested from the server and decoded:

        reply = urllib.request.urlopen(full_url).read()
        reply = reply.decode('utf-8')
        reply = json.loads(reply)

The reply is then used to extract the necessary currency data, which is stored in a dictionary. Notice that `datetime.datetime.fromtimestamp(reply['timestamp'])` takes the timestamp value returned by the server and converts it into a Python date object. Finally, the created dictionary is appended to the list:

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

After all of the days in april have been requested and the necessary data apended to the list, this list is saved to a file:

        with open("april_currency_data.dat",mode="wb") as currency_file:
            pickle.dump(april,currency_file)

With the data now in a file it can be accessed repeatedly without using up any more of our monthly API request allowance.

###currency_pyqt.py
This part of the task displays the data stored in the file as a line graph and presents the user with the option to convert an amount from one currency to another.

![][32]

It is separated into two classes:

1. CurrencyCompare - which is a subclass of FigureCanvas
2. MainWindow - which is a subclass of QMainWindow

####Currency Compare
`CurrencyCompare` is a widget which displays a line graph based on data stored in the file that was created previously. 

The code for this class is:

        class CurrencyCompare(FigureCanvas):
            def __init__(self):
                self.fig = Figure()
                self.ax = self.fig.add_subplot(1,1,1)
                super().__init__(self.fig)

                with open("april_currency_data.dat",mode="rb") as currency_file:
                    april = pickle.load(currency_file)

                self.CAD,self.AUD,self.GBP,self.NZD,self.EUR,dates = [],[],[],[],[],[]

                for day in april:
                    self.CAD.append(day['CAD'])
                    self.AUD.append(day['AUD'])
                    self.GBP.append(day['GBP'])
                    self.NZD.append(day['NZD'])
                    self.EUR.append(day['EUR'])
                    dates.append(day['date'])

                self.ax.set_ylabel("US Dollars")
                self.ax.set_xlabel("Date")
                self.ax.set_title("Currency Rates in April 2013")

                self.mpl_date = dte.date2num(dates)
                days_loc = dte.DayLocator()

                self.cad, = self.ax.plot_date(self.mpl_date,self.CAD,'b-',label="CAD")
                self.aus, = self.ax.plot_date(self.mpl_date,self.AUD,'g-',label="AUD")
                self.gbp, = self.ax.plot_date(self.mpl_date,self.GBP,'r-',label="GBP")
                self.nzd, = self.ax.plot_date(self.mpl_date,self.NZD,'k-',label="NZD")
                self.eur, = self.ax.plot_date(self.mpl_date,self.EUR,'y-',label="EUR")

                self.ax.legend(loc="upper left")

                date_fmt = dte.DateFormatter('%d/%m')
                self.ax.xaxis.set_major_formatter(date_fmt)
                self.ax.xaxis.set_major_locator(days_loc)
                self.fig.autofmt_xdate(rotation=90)
                self.ax.autoscale()
                self.fig.canvas.draw()

            def toggle_data(self,code):
                if code == "CAD":
                    if self.cad.get_visible():
                        self.cad.set_visible(False)
                    else:
                        self.cad.set_visible(True)
                elif code == "GBP":
                    if self.gbp.get_visible():
                        self.gbp.set_visible(False)
                    else:
                        self.gbp.set_visible(True)
                elif code == "AUD":
                    if self.aus.get_visible():
                        self.aus.set_visible(False)
                    else:
                        self.aus.set_visible(True)
                elif code == "NZD":
                    if self.nzd.get_visible():
                        self.nzd.set_visible(False)
                    else:
                        self.nzd.set_visible(True)
                elif code == "EUR":
                    if self.eur.get_visible():
                        self.eur.set_visible(False)
                    else:
                        self.eur.set_visible(True)
                self.fig.canvas.draw()

#####`__init__()` method
The constructor method created the initial state of the graph. The first three lines are:

        def __init__(self):
            self.fig = Figure()
            self.ax = self.fig.add_subplot(1,1,1)
            super().__init__(self.fig)

`self.fig = Figure()` creates the 'page' on which you will draw the graph. `self.ax = self.fig.add_subplot(1,1,1)` creates the axis for the particular graph you want to create. It is possible to have multiple subplots on a single figure. The values `1,1,1` refer to how many rows and columns there are on the figure and the final number refers to the individual figure plot number. 

Normally the call to `super().__init__()` is the first call in the constructor but because it requires the figure to be passed as a parameter it has to wait until after we have set this.

The currency data is then retrieved from the file:

        with open("april_currency_data.dat",mode="rb") as currency_file:
            april = pickle.load(currency_file)

Then lists for each individual currency that is going to be displayed are created by going through the list (`april`) retrieved from the file:

        self.CAD,self.AUD,self.GBP,self.NZD,self.EUR,dates = [],[],[],[],[],[]

        for day in april:
            self.CAD.append(day['CAD'])
            self.AUD.append(day['AUD'])
            self.GBP.append(day['GBP'])
            self.NZD.append(day['NZD'])
            self.EUR.append(day['EUR'])
            dates.append(day['date'])

The graph is then titled appropriately:

        self.ax.set_ylabel("US Dollars")
        self.ax.set_xlabel("Date")
        self.ax.set_title("Currency Rates in April 2013")

The next two lines convert the dates we retrieved from the file into the format the matplotlib uses internally and we also specific that we what ticks on the x-axis for each day:

        self.mpl_date = dte.date2num(dates)
        days_loc = dte.DayLocator()

The following lines plot each of the lines on the graph and generate a legend:

        self.cad, = self.ax.plot_date(self.mpl_date,self.CAD,'b-',label="CAD")
        self.aus, = self.ax.plot_date(self.mpl_date,self.AUD,'g-',label="AUD")
        self.gbp, = self.ax.plot_date(self.mpl_date,self.GBP,'r-',label="GBP")
        self.nzd, = self.ax.plot_date(self.mpl_date,self.NZD,'k-',label="NZD")
        self.eur, = self.ax.plot_date(self.mpl_date,self.EUR,'y-',label="EUR")

        self.ax.legend(loc="upper left")

Notice, that first parameter is the values for the x-axis (dates) and the second parameter the values for the y-axis (currency values). The final two parameters refer to the colour of the line and the label that each line should be given (this helps with generating the legend).

**Note the comma after each of attributes above:**

        self.cad,
        self.aus,
        etc.

**The reason for this is that `plot_date` returns a list of lines that are drawn and since we only want the first one we can unpack this by itsekf by using the above syntax.** 

The final section of code in this method is responsible for formatting the dates along the x-axis and drawing the graph:

        date_fmt = dte.DateFormatter('%d/%m')
        self.ax.xaxis.set_major_formatter(date_fmt)
        self.ax.xaxis.set_major_locator(days_loc)
        self.fig.autofmt_xdate(rotation=90)
        self.fig.canvas.draw()

#####`toggle_data()` method
This method shows or hides particular set of data from the graph based on the code parameter that is passed into the method.

        if code == "CAD":
            if self.cad.get_visible():
                self.cad.set_visible(False)
            else:
                self.cad.set_visible(True)
        elif code == "GBP":
            if self.gbp.get_visible():
                self.gbp.set_visible(False)
            else:
                self.gbp.set_visible(True)
        elif code == "AUD":
            if self.aus.get_visible():
                self.aus.set_visible(False)
            else:
                self.aus.set_visible(True)
        elif code == "NZD":
            if self.nzd.get_visible():
                self.nzd.set_visible(False)
            else:
                self.nzd.set_visible(True)
        elif code == "EUR":
            if self.eur.get_visible():
                self.eur.set_visible(False)
            else:
                self.eur.set_visible(True)
        self.fig.canvas.draw()

####Main Window
This class creates the main interface, displaying the graph and providing a way to convert an amount between currencies:

    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Currencies")

            self.currency_graph = CurrencyCompare()

            self.cad_checkbox = QCheckBox("Canada")
            self.aud_checkbox = QCheckBox("Australia")
            self.gbp_checkbox = QCheckBox("United Kingdom")
            self.nzd_checkbox = QCheckBox("New Zealand")
            self.eur_checkbox = QCheckBox("Eurozone")

            self.cad_checkbox.setChecked(True)
            self.aud_checkbox.setChecked(True)
            self.gbp_checkbox.setChecked(True)
            self.nzd_checkbox.setChecked(True)
            self.eur_checkbox.setChecked(True)

            self.checkbox_layout = QHBoxLayout()
            self.checkbox_layout.addWidget(self.cad_checkbox)
            self.checkbox_layout.addWidget(self.aud_checkbox)
            self.checkbox_layout.addWidget(self.gbp_checkbox)
            self.checkbox_layout.addWidget(self.nzd_checkbox)
            self.checkbox_layout.addWidget(self.eur_checkbox)

            self.from_currency_combo = QComboBox()
            self.to_currency_combo = QComboBox()

            currencies = ["Australian Dollar", "British Pound", "Canadian Dollar", "Euro", "New Zealand Dollar","United States Dollar"]

            self.from_currency_combo.addItems(currencies)
            self.to_currency_combo.addItems(currencies)

            self.amount_line_edit = QLineEdit()
            self.to_amount_line_edit = QLineEdit()
            self.convert_button = QPushButton("Convert")

            self.convert_layout = QHBoxLayout()

            self.convert_layout.addWidget(self.amount_line_edit)
            self.convert_layout.addWidget(self.from_currency_combo)
            self.convert_layout.addWidget(self.to_amount_line_edit)
            self.convert_layout.addWidget(self.to_currency_combo)

            self.to_amount_line_edit.setEnabled(False)


            self.layout = QVBoxLayout()

            self.layout.addWidget(self.currency_graph)
            self.layout.addLayout(self.checkbox_layout)
            self.layout.addLayout(self.convert_layout)
            self.layout.addWidget(self.convert_button)

            self.main_widget = QWidget()
            self.main_widget.setLayout(self.layout)

            self.setCentralWidget(self.main_widget)

            self.cad_checkbox.stateChanged.connect(self.toggle_canada)
            self.gbp_checkbox.stateChanged.connect(self.toggle_uk)
            self.aud_checkbox.stateChanged.connect(self.toggle_aus)
            self.nzd_checkbox.stateChanged.connect(self.toggle_nz)
            self.eur_checkbox.stateChanged.connect(self.toggle_euro)
            self.convert_button.clicked.connect(self.convert)

        def toggle_canada(self):
            self.currency_graph.toggle_data("CAD")

        def toggle_uk(self):
            self.currency_graph.toggle_data("GBP")

        def toggle_aus(self):
            self.currency_graph.toggle_data("AUD")

        def toggle_nz(self):
            self.currency_graph.toggle_data("NZD")

        def toggle_euro(self):
            self.currency_graph.toggle_data("EUR")

        def convert(self):
            amount = self.amount_line_edit.text()
            currency_from = self.from_currency_combo.currentIndex()
            currency_to = self.to_currency_combo.currentIndex()
            aud_dollar_value = self.currency_graph.AUD[29]
            gbp_dollar_value = self.currency_graph.GBP[29]
            cad_dollar_value = self.currency_graph.CAD[29]
            nzd_dollar_value = self.currency_graph.NZD[29]
            eur_dollar_value = self.currency_graph.EUR[29]

            dollar_values = [aud_dollar_value,gbp_dollar_value,cad_dollar_value,eur_dollar_value,nzd_dollar_value,1]

            dollars = float(amount) / dollar_values[currency_from]

            to_currency_amount = dollars * dollar_values[currency_to]
            self.to_amount_line_edit.setText("{0:.2f}".format(to_currency_amount))

#####`__init__()` method
The constructor method just generates the user interface. It will not be discussed further as you should be comfortable with PyQt before attempting this task.

#####`toggle_canada()` method et al.
These `toggle` methods are connected to the checkboxes for each country that are present in the interface and provide a way to show/hide the relevant data by calling the `toggle_data` method of the CurrencyCompare instance with the appropriate currency code:

        def toggle_canada(self):
            self.currency_graph.toggle_data("CAD")

        def toggle_uk(self):
            self.currency_graph.toggle_data("GBP")

#####`convert` method
The convert method is run when the user presses the convert button in the interface. It takes the currency amount to convert from the appropriate line edit:

        amount = self.amount_line_edit.text()

Then then currencies to convert to and from and found about by finding out the current index values for each of the combo boxes:

        currency_from = self.from_currency_combo.currentIndex()
        currency_to = self.to_currency_combo.currentIndex()

The US dollar values for each of the other currencies are then placed in a list. Notice that the final day of the month is used:

        aud_dollar_value = self.currency_graph.AUD[29]
        gbp_dollar_value = self.currency_graph.GBP[29]
        cad_dollar_value = self.currency_graph.CAD[29]
        nzd_dollar_value = self.currency_graph.NZD[29]
        eur_dollar_value = self.currency_graph.EUR[29]

        dollar_values = [aud_dollar_value,gbp_dollar_value,cad_dollar_value,eur_dollar_value,nzd_dollar_value,1]

The amount to convert is converted from the initial currency to US dollars:

        dollars = float(amount) / dollar_values[currency_from]

The dollar amount is then converted into the requested currency and this value is set as the text for the appropriate line edit:

        to_currency_amount = dollars * dollar_values[currency_to]
        self.to_amount_line_edit.setText("{0:.2f}".format(to_currency_amount))

##Code

You can find the code for this task on [GitHub][33]

##Further reading

Matplotlib is a huge library at it would be impossible to give more than a basic introduction here. I would recommend the following book on the topic:

- Tosi, S. 2009. [*Matplotlib for Python Developers*][34]. Birmingham: Packt.

I would suggest that the above book is the place to start but there is [documentation for matplotlib][35] available online.

There are two books available on PyQt:

- Harwani, B. M., 2012. [*Introduction to Python Programming and Developing GUI Applications with PyQT*][39]. Boston: Course Technology.
- Summerfield, M. 2008. [*RapidGUI Programming with Python and Qt*][40]. New York: Prentice Hall.

Both of them have some useful content but the Sumerfield book in particular is quite dated and does not include some of the recent improvements to PyQt. 

I would suggest that if you have worked through the [Python School][37] materials on PyQt then the [PyQt Class reference][38] is a better resource.

In addition, whilst the free access to the [Open Exchange Rates API][36] is limited there is other functionality that could be explored and used in additional tasks.

[27]: http://www.json.org
[31]: https://openexchangerates.org/signup/free
[32]: ../images/currency_converter.png
[33]: http://www.github.com/MrAGi/NewAdventuresinPython/
[34]: http://www.amazon.co.uk/Matplotlib-Python-Developers-S-Tosi/dp/1847197906/ref=sr_1_1?s=books&ie=UTF8&qid=1369599806&sr=1-1&keywords=Matplotlib+for+Python+Developers
[35]: http://matplotlib.org/contents.html
[36]: https://openexchangerates.org/documentation
[37]: http://www.pythonschool.net/eventdrivenprogramming/
[38]: http://pyqt.sourceforge.net/Docs/PyQt4/classes.html
[39]: http://www.amazon.co.uk/Introduction-Python-Programming-Developing-Applications/dp/1435460979/ref=sr_1_1?ie=UTF8&qid=1369599681&sr=8-1&keywords=Introduction+to+Python+Programming+and+Developing+GUI+Applications+with+PyQT
[40]: http://www.amazon.co.uk/Rapid-GUI-Programming-Python-Development/dp/0132354187/ref=sr_1_sc_1?s=books&ie=UTF8&qid=1369599777&sr=1-1-spell&keywords=RapidGUI+Programming+with+Python+and+Qt
[41]: ../installing.md#pyqt4
[42]: ../installing.md#matplotlib
[43]: ../installing.md#numpy
[44]: ../installing.md#network-x
[45]: ../installing.md#cx_freeze
[46]: ../installing.md#python-twitter





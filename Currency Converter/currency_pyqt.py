import sys
import pickle
from PyQt4.QtGui import *
import numpy as np
from matplotlib.figure import Figure
import matplotlib.dates as dte
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

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
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    mw.raise_()
    app.exec_()
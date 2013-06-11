import sqlite3
import sys
from PyQt4.QtGui import *
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

class CoffeeShopController:
    def __init__(self,path):
        self.path = path

    def query(self,sql,parameters=None):
        with sqlite3.connect(self.path) as self.db:
            cursor = self.db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            if parameters != None:
                cursor.execute(sql,parameters)
            else:
                cursor.execute(sql)
            results = cursor.fetchall()
            return results

    def product_totals(self,date):
        sql = """SELECT product.name, sum(product.price) as total
                FROM product, order_items, customer_order
                WHERE order_items.order_id = customer_order.order_id and 
                order_items.product_id = product.product_id and
                customer_order.date = ?
                GROUP BY product.name"""
        return self.query(sql,[date])

class CoffeeCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(1,1,1)
        super().__init__(self.fig)
        self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.fig.canvas.draw()

    def show_bar_graph(self,data,date):
        self.ax.clear()
        data_dict = dict(data)
        for i, key in enumerate(data_dict):
            self.ax.bar(i,data_dict[key])
        self.ax.set_xticks(np.arange(len(data_dict))+0.4)
        self.ax.set_xticklabels(list(data_dict.keys()))
        self.fig.autofmt_xdate()
        self.ax.set_title("Total Sales for {0}".format(date))
        self.ax.set_xlabel("Product")
        self.ax.set_ylabel("Amount (£)")
        self.fig.canvas.draw()

    def show_pie_chart(self,data,date):
        self.ax.clear()
        data_dict = dict(data)
        data = list(data_dict.values())
        labels = list(data_dict.keys())
        self.ax.pie(data,labels=labels,autopct='%1.1f%%')
        self.ax.set_title("Percentage Sales for {0}".format(date))
        self.fig.canvas.draw()

class CoffeeShopWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Graphing Examples")

        self.menu_bar = QMenuBar()
        self.tool_bar = QToolBar("Manage Databases")
        self.tab = QTabWidget()

        self.bar_canvas = CoffeeCanvas()
        self.pie_canvas = CoffeeCanvas()


        self.menu_bar = QMenuBar()
        self.file_menu = self.menu_bar.addMenu("File")
        self.open_database = self.file_menu.addAction("Open Database")

        self.bar_layout = QVBoxLayout()
        self.bar_layout.addWidget(self.bar_canvas)
        self.bar_widget = QWidget()
        self.bar_widget.setLayout(self.bar_layout)

        self.pie_layout = QVBoxLayout()
        self.pie_layout.addWidget(self.pie_canvas)
        self.pie_widget = QWidget()
        self.pie_widget.setLayout(self.pie_layout)

        self.tab.addTab(self.bar_widget,"Total Sales")
        self.tab.addTab(self.pie_widget,"Percentage Sales")

        self.tool_bar.addAction(self.open_database)
        self.addToolBar(self.tool_bar)
        self.setUnifiedTitleAndToolBarOnMac(True)

        self.setMenuWidget(self.menu_bar)
        self.setCentralWidget(self.tab)

        #connections
        self.open_database.triggered.connect(self.load_database)

    def load_database(self):
        path = QFileDialog.getOpenFileName(caption="Open Database")
        self.coffee_controller = CoffeeShopController(path)
        self.graph_data()

    def graph_data(self):
        totals = self.coffee_controller.product_totals("2013-05-27")
        self.pie_canvas.show_pie_chart(totals,"2012-05-27")
        self.bar_canvas.show_bar_graph(totals,"2012-05-27")


if __name__ == "__main__":
    application = QApplication(sys.argv)
    window = CoffeeShopWindow()
    window.show()
    window.raise_()
    application.exec_()

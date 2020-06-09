import json, sys, requests
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QInputDialog, QLabel, QLineEdit, QMainWindow, 
                                QMessageBox, QPushButton, QSizePolicy, QSlider, QStyle, QTableWidget, QTableWidgetItem, 
                                QVBoxLayout, QWidget)
from PySide2.QtMultimedia import QMediaPlayer
from PySide2.QtGui import QIcon

# URLS for Current and 5 day/ 3 hour forecast
urls = [
    "https://community-open-weather-map.p.rapidapi.com/weather",
    "https://community-open-weather-map.p.rapidapi.com/forecast"
]

# Query Strings for Current and 5 day/ 3 hour forecast
querystrings = [
    {"units":"%22metric%22","q":""}, # q = "city,country"
    {"q":""} # q = "city,country"
]

headers = {
    'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
    'x-rapidapi-key': ""
    }

class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setFixedSize(800, 600)
        self.setWindowTitle("Weather Buddy")
        self.setCentralWidget(widget)


class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.current_data = {
            "weather": {
                0: {
                    "main": "Main"
                }
            },
            "main": {
                "temp": "Temperature",
                "feels_like": "Feels Like",
                "temp_min": "Min Temp",
                "temp_max": "Max Temp",
            }

        }

        # JSON Data Table
        self.forecast_data = [0,8,16,24,32]

        # Search Bar
        self.input_city = QLineEdit()
        self.input_country = QLineEdit()
        search = QPushButton("Search")
        search.clicked.connect(self.searchWeather)

        # Search Bar Layout
        self.search_bar = QHBoxLayout()
        self.search_bar.addWidget(self.input_city)
        self.search_bar.addWidget(self.input_country)
        self.search_bar.addWidget(search)

        # Current Weather
        self.current_table = QTableWidget()
        self.current_table.setColumnCount(2)
        self.current_table.setHorizontalHeaderLabels(["Category", "Value"])
        self.current_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Forecast Weather
        self.forecast_table = QTableWidget()
        self.forecast_table.setColumnCount(5)
        self.forecast_table.setHorizontalHeaderLabels(["Day 1","Day 2","Day 3","Day 4","Day 5"])
        self.forecast_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Vertical Layout
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.search_bar)
        self.layout.addWidget(self.current_table)
        self.layout.addWidget(self.forecast_table)

        self.setLayout(self.layout)

    def searchWeather(self):
        city = self.input_city.text()
        country = self.input_country.text()
        q = city + "," + country
        querystrings[0]["q"] = querystrings[1]["q"] = q
        self.response_current = requests.request("GET",urls[0],headers=headers,params = querystrings[0])
        self.response_current = self.response_current.json()
        self.response_forecast = requests.request("GET",urls[1],headers=headers,params = querystrings[1])
        self.response_forecast = self.response_forecast.json()
        
        self.currentWeather()
        self.forecastWeather()

    def currentWeather(self):
        self.current_table.setRowCount(0)
        item = 0
        self.current_table.insertRow(item)
        self.current_table.setItem(item, 0, QTableWidgetItem(self.current_data["weather"][0]["main"]))
        self.current_table.setItem(item, 1, QTableWidgetItem(str(self.response_current["weather"][0]["main"])))
        item += 1
        for resp, desc in self.current_data["main"].items():
            self.current_table.insertRow(item)
            self.current_table.setItem(item, 0, QTableWidgetItem(desc))
            self.current_table.setItem(item, 1, QTableWidgetItem(str(round(self.response_current["main"][resp] - 273))))
            item += 1
        

    def forecastWeather(self):
        self.forecast_table.setRowCount(1)
        column = 0
        for data in self.forecast_data:
            self.forecast_table.setItem(0, column, QTableWidgetItem(str(self.response_forecast["list"][data]["weather"][0]["main"])))
            column += 1




def main():
    f = open("SECRET_KEY.txt", "r")
    headers['x-rapidapi-key'] = f.read()
    f.close()

    app = QApplication(sys.argv)
    widget = Widget()
    window = MainWindow(widget)
    window.show()

    sys.exit(app.exec_())



if __name__ == "__main__":
    main()